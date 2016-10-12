# -*- coding: utf-8 -*-

import re
from unidecode import unidecode

from field_const import Fields


# =============================================================================
# CLEANERS & DECORATORS
# =============================================================================

def trash(text):
    return not re.match('^(\s*|\\n|\\xa0)$', text)


def clean(text):
    processed = re.sub('\\n|\\r', ' ', text)
    processed = re.sub('\s+', ' ', processed)
    processed = processed.strip(': ,;')
    return processed


def concat_keys(func):
    """
    original result: {
        key1: val1,
        key2: val2
    }
    wrapped result: {
        <field_name>_key1: val1,
        <field_name>_key2: val2
    }
    """
    def func_wrapper(field_name, field_val):
        result = func(field_name, field_val)
        return dict([('{}_{}'.format(field_name, k), v)
                     for k, v in result.iteritems()])
    return func_wrapper


# =============================================================================
# FIELD PARSERS
# =============================================================================

# @concat_keys
def address(field_name, address):
    """
    Extracts the address parameters from a full address
    """
    house_num_short = {
    }

    f1, f2, street = address.split(' ', 2)
    street_re = r'^([^\d]+|\d.+)\s((HRSZ\:|\d).*)'
    street_match = re.search(street_re, street)
    if street_match:
        street = street_match.group(1)
        # The house number will be shortened now
        house_num_comp = []
        for comp in street_match.group(2).replace('.', '').split():
            house_num_comp.append(house_num_short.get(unidecode(comp), comp))
        house_num = ' '.join([c for c in house_num_comp if c])
    else:
        house_num = ''
    city, zip_code = (f1, f2) if f2.isdigit() else (f2, f1)
    city = city.strip(', ').lower().capitalize()

    return {
        Fields.STREET: street,
        Fields.ZIP: zip_code,
        Fields.HOUSE_NUM: house_num,
        Fields.CITY: city,
    }


def task_type(field_name, task_type):
    """
    We had too many task types like L-MDF Multiservice point (KOAX) [NG]
    Since we can only have a maximum of 64 of these otherwise the UI crashes,
    we need to remove the unnecessary parts so that we can have less elements
    """
    def _extract_keywords(*args):
        kws = (u'KOAX', u'Optika', u'Réz')
        for arg in args:
            for kw in kws:
                if unidecode(kw.lower()) in unidecode(arg).lower():
                    return kw
        return None

    result = {}
    try:
        data = map(lambda x: x.strip(' )]'), re.split('[\(\[]', task_type))
        root_type, extra_data = data[0], data[1:]
        extra = _extract_keywords(*extra_data)
        extra = ' ({})'.format(extra) if extra else ''
        result = {
            Fields.TASK_TYPE: root_type + extra
        }
    except Exception:
        pass

    return result

# =============================================================================
# POST PROCESSORS
# =============================================================================


def _extract_col_adj_values(soup, header, next_row_cell=None):
    """
    Extracts the key and value vertically (adjacent cells).
    Key is taken as a header, value is a list of values in the next rows after
    the header
    """
    extracted = []
    for td in soup.find_all('td'):
        texts = filter(trash, td.find_all(text=True))
        if len(texts) == 1 and \
                unidecode(texts[0].strip().strip('":')) == header:
            idx = next_row_cell or filter(lambda x: x.name == 'td',
                                          td.parent.contents).index(td)
            next_tr = td.parent.findNext('tr')
            while next_tr and next_tr.name == 'tr':
                next_tr_cells = next_tr.find_all('td')
                if len(next_tr_cells) < idx:
                    break
                data = filter(trash, map(clean, next_tr_cells[idx].find_all(text=True)))
                extracted.append(' '.join(data))
                next_tr = next_tr.next_sibling
            break
    return extracted


def extract_collectable_money(soup, extracted_data):
    result = {}
    for td in soup.find_all('td'):
        if 'Begyujtendo osszeg' in map(lambda x: unidecode(x).strip('": '),
                                       td.find_all(text=True)):
            next_td = td.next_sibling
            amount = next_td.find_all(text=True)[0]
            result = {Fields.COLLECTABLE_MONEY: amount}
            break

    return result


def extract_bracketed(soup, extracted_data):
    KEY_MAP = {
        'MT_ID': Fields.MT_ID,
    }
    result = {}
    for td in soup.find_all('td'):
        text = td.text or ''
        bracketed = re.findall('\[([^\]]+)=([^\]]+)\]', text)
        if bracketed:
            for data in bracketed:
                key, value = map(unicode.strip, data)
                if key in KEY_MAP:
                    result[KEY_MAP[key]] = value
    return result


def extract_address(soup, extracted_data):
    """
    To extract the address from given in a non-standard format
    e.g. test25.html
    """
    result = {}
    for td in soup.find_all('td'):
        if len(td.parent.find_all('td')) == 3 and \
                'Letesitesi cim' in map(lambda x: unidecode(x).strip('": '),
                                        td.find_all(text=True)):
            next_td = td.next_sibling.next_sibling
            address = next_td.find_all(text=True)[0]
            result = {Fields.ADDR1: address.strip()}
            break

    return result


def extract_remark(soup, extracted_data):
    result = {}
    # Triplets, first value is the word to look for,
    # second value is the column in the next row to look
    # third value is the exeptions if the result starts with, ignore all
    words_to_seek = (
        ['Leiras'],
        ['Megjegyzesek', 3, ('IMDB', 'EGYSEGES EGYEDI')],
        ['Megjegyzesek'],
    )

    for lookup in words_to_seek:
        word, col, exceptions = lookup + [None]*(3-len(lookup))
        remarks = _extract_col_adj_values(soup, word, col)
        if remarks:
            if exceptions and unidecode(remarks[0]).startswith(exceptions):
                continue
            # We need only the first row (?)
            result = {Fields.REMARKS: remarks[0]}
            break

    return result


def extract_task_type(soup, extracted_data):
    """
    Required for yet again some weird format where the task type and the value
    are in two separate rows in the first column
    + another test case (test31.html)
    """
    result = {}
    if extracted_data.get('Feladat', '').startswith('Egyeztetett'):
        task = _extract_col_adj_values(soup, 'Feladat')
        # We need the first row only
        # First cell of the first row
        result = {Fields.TASK_TYPE: task[0]}

    return result


def extract_device_params(soup, extracted_data):
    """
    Extracts the device parameters like S/N, type, etc.
    Different files require different methods, so we need to try multiple times
    before having a successful result
    """
    devices = \
        _extract_devices_method1(soup, extracted_data) or \
        _extract_devices_method2(soup, extracted_data) or \
        _extract_devices_method3(soup, extracted_data) or \
        {}

    # Filter the cards out - we don't need them
    devices = filter(
        lambda dev: dev[Fields.DEV_SN][0:3] not in ('014', '020'), devices)

    devices = filter(
        lambda dev: not re.match('^\s*$', dev[Fields.DEV_SN]), devices)

    return {Fields.DEVICES: devices} if devices else {}


def _extract_devices_method1(soup, extracted_data):
    """
    Operating with the extracted data
    """
    devices = []

    if 'STB azonosito nyilvantartas szerint' in extracted_data \
            and extracted_data['STB azonosito nyilvantartas szerint']:
        device = {
            Fields.DEV_SN:
                extracted_data['STB azonosito nyilvantartas szerint'],
            Fields.DEV_CARD_SN:
                extracted_data['Kartya azonosito nyilvantartas szerint'],
        }
        devices.append(device)

    return devices


def _extract_devices_method2(soup, extracted_data):
    """
    Method 2
    This method extracts data from the type of document seen in e.g.
    test2.html, test21.html, test22.html, test23.html, test4.html,
    test6.html
    """
    KEY_MAP = {
        'Tipus': Fields.DEV_TYPE,
        'Eszkoz vonalkod': Fields.DEV_SN,
        'Eszkoz igenybevetel': Fields.DEV_OWNERSHIP,
    }

    def get_field(for_key):
        for key in KEY_MAP:
            if key in unidecode(for_key):
                return KEY_MAP[key]

    devices = []

    for td in soup.find_all('td'):
        if td.find('td'):
            continue
        text = unidecode(td.text)
        if 'Eszkoz vonalkod' in text and 'Tipus' in text:
            device = {}
            data = td.find_all(text=True)
            for idx, curr_field in enumerate(data):
                field = get_field(curr_field)
                if field and field in device:
                    if Fields.DEV_SN in device:
                        devices.append(device)
                    device = {}
                if field:
                    try:
                        value = data[idx+1]
                        if get_field(value):
                            value = None
                    except IndexError:
                        value = None
                    if value:
                        device[field] = value

            if Fields.DEV_SN in device:
                devices.append(device)

    return devices


def _extract_devices_method3(soup, extracted_data):
    """
    Method 3. Test27, Test7, Test6, Test23
    """
    devices = []

    method2_res = _extract_col_adj_values(soup, 'Vonalkod')
    if method2_res:
        serials = set()
        # ei = [v[0] if v else ''
        #       for v in _extract_col_adj_values(soup, 'Eszkozigeny')]
        tipus = _extract_col_adj_values(soup, 'Tipus')
        vonalkod = method2_res
        # cikkszam = _extract_col_adj_values(soup, 'Cikkszam')

        for idx, t in enumerate(tipus):
            if vonalkod[idx] not in serials:
                device = {
                    Fields.DEV_TYPE: t,
                    # Fields.DEV_OWNERSHIP: ei[idx],
                    Fields.DEV_SN: vonalkod[idx],
                }
                serials.add(vonalkod[idx])
                devices.append(device)

    return devices


# =============================================================================
# DATA CLEANERS ON THE FINAL DATA
# =============================================================================

def clean_name(processed_data):
    name1 = processed_data[Fields.NAME1]
    name2 = processed_data.get(Fields.NAME2)
    result = {}
    if 'ERROR' in name1 and name2 is not None:
        result = {Fields.NAME1: name2}
    return result


def clean_task_type(processed_data):
    """
    Creates a task type list and cleans multiple task types.
    """
    def _clean(task_type):
        task_type = task_type.strip()
        return re.sub(u'Alvállalkozó\s?\-\s?', u'', task_type)

    task_type = processed_data[Fields.TASK_TYPE]
    result = {}
    tasks = re.findall('[HL]-.+?(?=[HL]-|$)', task_type)
    if tasks:
        tasks = map(_clean, tasks)
        seen = set()
        tasks = [t for t in tasks if not (t in seen or seen.add(t))]
        if len(tasks) > 1:
            result[Fields.TASK_TYPE_LIST] = tasks
        result[Fields.TASK_TYPE] = ' '.join(tasks)
    return result

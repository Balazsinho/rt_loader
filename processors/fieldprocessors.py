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

            parent_table = td.parent
            while parent_table.name != 'table':
                parent_table = parent_table.parent

            rows = parent_table.find_all('tr')
            for row in (rows[1:] if len(rows) > 1 else rows):  # Skip the header
                next_tr_cells = row.find_all('td')
                if len(next_tr_cells) < idx:
                    break
                data = filter(trash, map(clean, next_tr_cells[idx].find_all(text=True)))
                extracted.append(' '.join(data))
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
        bracketed = re.findall('\[([^\]]+)=([^\]]+)\]', text) or []
        for data in bracketed:
            key, value = map(unicode.strip, data)
            if key in KEY_MAP:
                result[KEY_MAP[key]] = value
    return result


def extract_address(soup, extracted_data):
    """
    To extract the address from given in a non-standard format
    e.g. test25.html, test37.html, test38.html
    """
    result = {}
    for td in soup.find_all('td'):
        texts = map(clean, filter(trash, td.find_all(text=True)))
        if len(texts) == 1 and \
                unidecode(texts[0]) == 'Letesitesi cim' and \
                len(td.parent.find_all('td')) == 3:
            row = td.parent.find_all('td')
            addr_td = row[2]
            address = addr_td.find_all(text=True)[0]
            result = {Fields.ADDR1: clean(address)}
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
        _extract_devices_method4(soup, extracted_data) or \
        {}

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
        }
        devices.append(device)
        card = extracted_data['Kartya azonosito nyilvantartas szerint']
        if card:
            devices.append({Fields.DEV_SN: card,
                            Fields.DEV_TYPE: 'CONAX SMART CARD'})

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

    def is_card(device):
        return Fields.DEV_SN in device and \
            'CARD' in device.get(Fields.DEV_TYPE)

    def get_field(for_key):
        for key in KEY_MAP:
            if key in unidecode(for_key):
                return KEY_MAP[key]

    devices = []
    cards = []

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
                    if is_card(device):
                        cards.append(device)
                    elif Fields.DEV_SN in device:
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
                        device[field] = value.strip()
                if field == Fields.DEV_TYPE:
                    elements = data[idx].split(')')
                    if len(elements) == 2:
                        device[Fields.DEV_ACTION] = elements[0].strip().strip('(')

            if is_card(device):
                cards.append(device)
            if Fields.DEV_SN in device:
                devices.append(device)

    #while cards:
    #    card = cards.pop()
    #    for device in devices:
    #        if Fields.DEV_CARD_SN not in device and \
    #                card.get(Fields.DEV_ACTION) == device.get(Fields.DEV_ACTION):
    #            card_sn = card[Fields.DEV_SN]
    #            if card_sn:
    #                device[Fields.DEV_CARD_SN] = card_sn
    #            break

    return devices + cards


def _extract_devices_method3(soup, extracted_data):
    """
    Method 3. Test27, Test7, Test6, Test23
    """
    devices = []

    method3_res = _extract_col_adj_values(soup, 'Vonalkod')
    if method3_res:
        serials = set()
        tipus = _extract_col_adj_values(soup, 'Tipus')
        vonalkod = method3_res

        for idx, t in enumerate(tipus):
            if vonalkod[idx] not in serials:
                device = {
                    Fields.DEV_TYPE: (t or '').strip(),
                    Fields.DEV_SN: vonalkod[idx],
                }
                serials.add(vonalkod[idx])
                devices.append(device)

    return devices


def _extract_devices_method4(soup, extracted_data):
    """
    Method 4. Test37, test25, test28, test31
    """
    devices = []

    tipus = _extract_col_adj_values(soup, 'Vegberendezes')
    if tipus:
        sns = _extract_col_adj_values(soup, 'Sorozatszam')
        serials = set()

        for idx, t in enumerate(tipus):
            if t and sns[idx]:
                device = {
                    Fields.DEV_TYPE: (t or '').strip(),
                    Fields.DEV_SN: sns[idx],
                }
                serials.add(sns[idx])
                devices.append(device)

    return devices


def extract_agreed_time(soup, extracted_data):
    time_from = _extract_col_adj_values(soup, 'Egyeztetett ido (-tol)')
    if time_from:
        time_to = _extract_col_adj_values(soup, '(-ig)')
        return {
            Fields.AGREED_TIME_FROM: time_from.pop(),
            Fields.AGREED_TIME_TO: time_to.pop(),
        }
    return {}


def extract_extra_devices(soup, extracted_data):
    """
    Extracts the extra devices e.g. tablet, TV
    test45
    """
    devices = []
    for td in soup.find_all('td'):
        if unidecode(td.text).strip().startswith('Eszkoz nev:'):
            m = re.search(u'Eszköz név:(.*)\s*\-\s*Cikkszám:(.*)', td.text)
            if m:
                name, code = map(lambda x: x.strip(), m.groups())
                devices.append({Fields.EXTRA_DEV_CODE: code,
                                Fields.EXTRA_DEV_TYPE: name})

    return {Fields.EXTRA_DEVICES: devices} if devices else {}


def extract_title(soup, extracted_data):
    """
    Extract title from the mail
    """
    result = {}
    title = soup.find('title')
    if title:
        texts = filter(trash, title.find_all(text=True))
        title = map(clean, texts)[0] if texts else None
        result = {Fields.TITLE: title}

    return result


def extract_task_nr(soup, extracted_data):
    """
    Extracts the raw task NR when they send it in a row that has 3 cells,
    the first one containing "Munkarendeles"
    """
    result = {}
    for td in soup.find_all('td'):
        texts = map(clean, filter(trash, td.find_all(text=True)))
        if len(texts) == 1 and \
                unidecode(texts[0]) == 'Jegyazonosito-Task Nr':
            row = map(clean, filter(trash, td.parent.find_all(text=True)))
            if len(row) != 3:
                break
            result = {Fields.TICKET_ID: row[2]}
            break

    return result


def extract_client_id(soup, extracted_data):
    """
    Extracts the raw client ID when they send it in a row that has 5 cells
    e.g. test44
    """
    result = {}
    for td in soup.find_all('td'):
        texts = map(clean, filter(trash, td.find_all(text=True)))
        if len(texts) == 1 and \
                unidecode(texts[0]) == 'Ugyfelszam':
            row = map(clean, filter(trash, td.parent.find_all(text=True)))
            result = {Fields.MT_ID: row[-1]}
            break

    return result


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


def clean_phones(processed_data):
    phone1 = processed_data.get(Fields.PHONE1, '')
    phone2 = processed_data.get(Fields.PHONE2, '')
    if phone1 and not re.match('[\+\d,\s]+', phone1):
        del processed_data[Fields.PHONE1]
    if phone2 and not re.match('[\+\d,\s]+', phone2):
        del processed_data[Fields.PHONE2]
    return {}


def clean_task_type(processed_data):
    """
    Creates a task type list and cleans multiple task types.
    """
    def _clean(task_type):
        task_type = task_type.strip()
        return re.sub(u'Alvállalkozó\s?\-\s?', u'', task_type)

    task_type = processed_data.get(Fields.TASK_TYPE) or \
        processed_data[Fields.TITLE]
    result = {}
    tasks = re.findall('[HL]-.+?(?=[HL]-|$)', task_type) or [task_type]
    if tasks:
        tasks = map(_clean, tasks)
        seen = set()
        tasks = [t for t in tasks if not (t in seen or seen.add(t))]
        if len(tasks) > 1:
            result[Fields.TASK_TYPE_LIST] = tasks
        result[Fields.TASK_TYPE] = ' '.join(tasks)
    return result


def clean_mt_id(processed_data):
    if Fields.MT_ID not in processed_data and \
            Fields.TICKET_ID in processed_data:
        return {Fields.MT_ID: processed_data[Fields.TICKET_ID]}
    return {}


def agreed_time_raw(processed_data):
    raw_time = processed_data.get(Fields.AGREED_TIME_RAW)
    if raw_time and re.search('^\d{4}.*', raw_time):
        components = raw_time.split(' - ')
        if len(components) == 2:
            time_from, time_to = components
        elif len(components) == 1:
            time_from = components[0]
            time_to = None
        else:
            raise Exception('Could not clean raw agreed time {}'
                            ''.format(raw_time))
        return {
            Fields.AGREED_TIME_FROM: time_from,
            Fields.AGREED_TIME_TO: time_to,
        }
    return {}

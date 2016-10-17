# -*- coding: utf-8 -*-

from unidecode import unidecode
from bs4 import BeautifulSoup
from processors import field_map
from processors import fieldprocessors as postparsers
from processors.fieldprocessors import clean, trash


class MailParser(object):

    POST_PARSERS = (
        postparsers.extract_remark,
        postparsers.extract_task_type,
        postparsers.extract_device_params,
        postparsers.extract_collectable_money,
        postparsers.extract_address,
        postparsers.extract_bracketed,
    )

    CLEANERS = (
        postparsers.clean_name,
        postparsers.clean_task_type,
        postparsers.clean_mt_id,
    )

    def __init__(self, logger):
        self.logger = logger

    def extract_raw(self, mail_contents):
        """
        Extract the raw data with multiple methods.
        There is a large amount of trash generated given the obscure nature
        of the email that needs to be processed.
        """
        soup = BeautifulSoup(mail_contents, 'lxml')
        extracted_data = {
            field_map.Fields.TITLE: self._extract_title(soup)
        }

        for row in soup.find_all('tr'):
            cells = row.find_all('td')
            self._update(extracted_data,
                         self.extract_kv_from_cells(cells))
            for cell in cells:
                data_elements = self._extract_data_from_cell(cell)
                self._update(extracted_data,
                             self.extract_kv_from_list(data_elements))
                for d in data_elements:
                    self._update(extracted_data,
                                 self.extract_kv_from_str(d))

        for parser in self.POST_PARSERS:
            try:
                extracted_data.update(parser(soup, extracted_data))
            except Exception as e:
                self.logger.warning('{} postparser error: {}'
                                    ''.format(parser.__name__, str(e)))

        return extracted_data

    def _update(self, data, new_data):
        for key, val in new_data.iteritems():
            if val or (key not in data):
                data[key] = val

    def parse(self, mail_contents):
        """
        Extracts the data in multiple possible ways. After the raw data is
        gathered, it extracts the usable items from the data, also maps
        the usable items to the internal common field_map.
        """
        # Extract the data first
        extracted_data = self.extract_raw(mail_contents)

        # All data extracted, now we need to filter the usable stuff out of
        # the large dataset. We also do the mapping to internal values at
        # this point.
        processed_data = {}
        for k, v in extracted_data.iteritems():
            if field_map.is_field_usable(k):
                if k in field_map.FINAL_FIELDS or k not in processed_data:
                    processed_data[field_map.mapped_field(k)] = v
            else:
                self.logger.debug(u'Mező nem ismert - KULCS: {} - ÉRTÉK: {}'
                                  u''.format(k, v))

        # We post process the data elements to squeeze some additional data
        # out.
        self.expand_data(processed_data)
        self.clean_data(processed_data)

        if len(processed_data.keys()) < 3:
            raise Exception(u'Ismeretlen levél, kérlek ellenőrizd!')

        # All done, go for data loading
        return processed_data

    def expand_data(self, data):
        """
        Calls the additional processors on each data element if there are any
        """
        for k, v in data.copy().iteritems():
            for proc in field_map.processors(k):
                data.update(proc(k, v))

    def clean_data(self, data):
        """
        Calls the data cleaners on the already processed data - final step
        """
        for cleaner in self.CLEANERS:
            data.update(cleaner(data))

    def extract_kv_from_str(self, field):
        """
        Checks if a string is in a key:value format
        It is considered that if there is only one colon in the string.
        The part before the colon is the key, the part after is the value
        """
        def callback(data):
            return data.strip()

        return self._generate_kv_pairs_from_data(field.split(':', 1), callback)

    def extract_kv_from_list(self, values):
        """
        It checks if a list of values is in pairs. Creates key:value pairs
        out of the list pairs.
        """
        def callback(data):
            return data.strip()

        return self._generate_kv_pairs_from_data(values, callback)

    def extract_kv_from_cells(self, cells):
        """
        Checks if the cells are in pairs. Creates key:value items from the
        pairs
        """
        def callback(data):
            return ' '.join(self._extract_data_from_cell(data))

        return self._generate_kv_pairs_from_data(cells, callback)

    def _generate_kv_pairs_from_data(self, data, callback):
        """
        Gets iterable data. If the data is divisible by 2, it'll create
        key:value pairs out of the adjoining items and return all in a dict
        """
        parsed_data = {}
        if len(data) > 1 and len(data) % 2 == 0:
            for i in range(0, len(data), 2):
                key = callback(data[i])
                value = callback(data[i+1])
                if type(key) is not str:
                    key = unidecode(key)
                parsed_data.update({key.strip(): value})
        return parsed_data

    def _extract_data_from_cell(self, cell_contents, encode_ascii=False):
        """
        Extracts and cleans the data coming from an individual cell
        - excludes any content that is only whitespace or '\n' or \xa0
        - removes leading/trailing whitespaces, commas
        - removes newlines
        - removes multiple consecutive whitespaces
        """

        texts = filter(trash, cell_contents.find_all(text=True))
        return map(clean, texts)

    def _extract_title(self, soup):
        title = soup.find('title')
        if title:
            title = self._extract_data_from_cell(title)
            title = title[0] if title else None
        else:
            self.logger.debug('<title> mezőt nem találtam')

        return title

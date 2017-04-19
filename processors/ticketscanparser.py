import re

from scanparserbase import ScanParserBase


class TicketScanParser(ScanParserBase):

    def extract_task_nr(self, raw_extr):
        """
        Extracts the WFMS ID from the raw OCR data
        """
        possible_keywords = (r'sk\snr',
                             r'hiba[ij]egy\sazon\S+')
        longest_id = 0
        wfms_id = None
        for kw in possible_keywords:
            wfms_ids = re.findall(r'(' + kw + r'\:\s*\S{7,})',
                                  raw_extr, re.I)
            for raw_id in wfms_ids:
                temp_id = re.sub(r'\D', '', raw_id)
                if len(temp_id) > longest_id:
                    wfms_id = temp_id
                    longest_id = len(temp_id)

        try:
            wfms_id, postfix = wfms_id[:8], wfms_id[8:]
        except:
            postfix = None

        if postfix:
            return ['{}-{}'.format(wfms_id, postfix),
                    '{}.{}'.format(wfms_id, postfix)]
        elif wfms_id:
            return [wfms_id]
        else:
            return []

    def task_nr_from_raw(self, raw_file):
        raw_extr, img = self.extract_ocr(raw_file)
        return self.extract_task_nr(raw_extr), img

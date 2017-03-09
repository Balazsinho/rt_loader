import codecs
import os
import unittest

from settings import PROJECT_DIR
from processors.ticketscanparser import TicketScanParser
from loggermock import LoggerMock


class TestTicketScanning(unittest.TestCase):

    def setUp(self):
        self.logger = LoggerMock()
        self.parser = TicketScanParser(self.logger, debug=True)

    def _get_test_file(self, filename):
        return codecs.open(
            os.path.join(PROJECT_DIR, 'files', 'test',
                         'ticket_scan', filename))

    def _test_file1(self):
        """
        Normal quality scan, slightly slanted
        """
        with self._get_test_file('test1.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['63124090-653', '63124090.653'])

    def _test_file2(self):
        """
        Pale scan, slightly slanted
        """
        with self._get_test_file('test2.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, [])

    def _test_file3(self):
        """
        Pale scan, slightly slanted, bit ghostly image
        """
        with self._get_test_file('test3.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['66057701-436', '66057701.436'])

    def _test_file4(self):
        """
        6 and 9 in task nr are harder to read
        """
        with self._get_test_file('test4.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['65559982-469', '65559982.469'])

    def _test_file5(self):
        """
        task nr numbers are a bit fucked up
        """
        with self._get_test_file('test5.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['65862960-446', '65862960.446'])

    def _test_file6(self):
        """
        Pale and weird numbers
        """
        with self._get_test_file('test6.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['65932223-439', '65932223.439'])

    def _test_file7(self):
        """
        Low quality scan
        """
        with self._get_test_file('test7.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, [])

    def _test_file8(self):
        """
        Bit more slanted
        """
        with self._get_test_file('test8.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['63363845-1063', '63363845.1063'])

    def _test_file9(self):
        """
        Low resolution scan
        """
        with self._get_test_file('test9.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, [])

    def test_file10(self):
        """
        Different ticket
        """
        with self._get_test_file('test10.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['68872012.1', '68872012-1'])

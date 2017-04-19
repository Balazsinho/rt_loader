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

    def test_file1(self):
        """
        Normal quality scan, slightly slanted
        """
        with self._get_test_file('test1.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['63124090-653', '63124090.653'])

    def test_file2(self):
        """
        Pale scan, slightly slanted
        """
        with self._get_test_file('test2.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, [])

    def test_file3(self):
        """
        Pale scan, slightly slanted, bit ghostly image
        """
        with self._get_test_file('test3.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['66057701-436', '66057701.436'])

    def test_file4(self):
        """
        6 and 9 in task nr are harder to read
        """
        with self._get_test_file('test4.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['65559982-469', '65559982.469'])

    def test_file5(self):
        """
        task nr numbers are a bit fucked up
        """
        with self._get_test_file('test5.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['65862960-446', '65862960.446'])

    def test_file6(self):
        """
        Pale and weird numbers
        """
        with self._get_test_file('test6.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['65932223-439', '65932223.439'])

    def test_file7(self):
        """
        Low quality scan, parser picks up bs
        """
        with self._get_test_file('test7.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['13111338-1102', '13111338.1102'])

    def test_file8(self):
        """
        Bit more slanted
        """
        with self._get_test_file('test8.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['63363845-1063', '63363845.1063'])

    def test_file9(self):
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
        self.assertListEqual(wfms_id, ['68872012-1', '68872012.1'])

    def test_file11(self):
        """
        There's bullshit between ID and identifier text
        """
        with self._get_test_file('test11.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['66549306-368', '66549306.368'])

    def test_file12(self):
        """
        Test with 4 digits after the dash
        """
        with self._get_test_file('test12.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['65451392-1756', '65451392.1756'])

    def test_file13(self):
        """
        The text for task nr was read as hsk-nr
        """
        with self._get_test_file('test13.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['62977191-549', '62977191.549'])

    def test_file14(self):
        """
        Trash between task nr placeholder and actual task nr
        """
        with self._get_test_file('test14.pdf') as raw_file:
            wfms_id, _ = self.parser.task_nr_from_raw(raw_file)
        self.assertListEqual(wfms_id, ['66549306-368', '66549306.368'])

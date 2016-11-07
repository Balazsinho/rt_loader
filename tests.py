# -*- coding: utf-8 -*-

import os
import codecs
import unittest

from settings import PROJECT_DIR
from processors.mailparser import MailParser
from downloader.mail import Mail
from utils.pprinter import PPrinter


class LoggerMock(object):

    def __init__(self):
        self.msgs = []

    def log(self, msg):
        self.msgs.append(msg)

    def debug(self, msg):
        self.log(msg)

    def info(self, msg):
        self.log(msg)

    def warning(self, msg):
        print 'WARNING ' + msg
        self.log(msg)

    def error(self, msg):
        print 'ERROR ' + msg
        self.log(msg)


class TestRawMailParsing(unittest.TestCase):

    """
    Test the processing of the raw mail data
    """

    def setUp(self):
        self.logger = LoggerMock()

    def _get_mail_file(self, filename):
        return codecs.open(
            os.path.join(PROJECT_DIR, 'files', 'test',
                         'raw', filename), 'r').readlines()


class TestMailParsing(unittest.TestCase):

    """
    Test the pickup and extraction of the HTML data
    """

    def setUp(self):
        self.logger = LoggerMock()
        self.parser = MailParser(self.logger)
        self.maxDiff = None

    def _get_mail_file(self, filename):
        return codecs.open(
            os.path.join(PROJECT_DIR, 'files', 'test',
                         'html', filename), 'r').read()

    def test_file1(self):
        f = self._get_mail_file('test1.html').replace('<!-- o ignored -->', '')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'1148 BUDAPEST Fogarasi út 57 FS em. 1 ajtó',
            'city': u'Budapest',
            'house_num': u'57 FS em 1 ajtó',
            'mt_id': u'459645584',
            'name1': u'Fifo Kft.',
            'order_num': u'7264734',
            'phone1': u'+36309892944',
            'street': u'Fogarasi út',
            'task_type': (u'L-Szolgáltatás üzembehelyezés '
                          u'(Optika)'),
            'ticket_id': u'61728463-1343',
            'zip': u'1148'
        }

        self.assertDictEqual(output, expected)

    def test_file2(self):
        f = self._get_mail_file('test2.htm')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'FEGYVERNEK 5231 Háy Mihály út 36. /A',
            'agreed_time': u'2016-05-12 17:00:00 - 2016-05-12 18:00:00',
            'city': u'Fegyvernek',
            'date_created': u'2016-05-06 10:38:50',
            'devices': [
                {'device_sn': u'ZTEEF01BB415308',
                 'device_type': u'ZXV10 H201L'},
                {'device_ownership': u'Bérelt',
                 'device_sn': u'00595002853',
                 'device_type': u'INTEK-S50CX DVB-S2 MPEG4 SD SET TOP BOX'},
                {'device_ownership': u'Bérelt',
                 'device_sn': u'00595140246',
                 'device_type': u'INTEK-S50CX DVB-S2 MPEG4 SD SET TOP BOX'},
                {'device_ownership': u'Bérelt',
                 'device_sn': u'00595262911',
                 'device_type': u'INTEK-S50CX DVB-S2 MPEG4 SD SET TOP BOX'},
            ],
            'house_num': u'36 /A',
            'mt_id': u'22222222',
            'name1': u'Gácsi Dénes',
            'order_num': u'2d323535363432373833363832323330',
            'oss_id': u'33333333',
            'phone1': u'+36703654519',
            'phone2': u'56481562',
            'req_type': u'Műszaki Hozzáférés - [MÓD] - SATTV',
            'street': u'Háy Mihály út',
            'task_type': u'L-Helyszíni Feladat MULTI-DVBS [SPA]',
            'ticket_id': u'60446435-799',
            'title': u'Szerelési lap',
            'zip': u'5231'
        }

        self.assertDictEqual(output, expected)

    def test_file3(self):
        f = self._get_mail_file('test3.htm')
        output = self.parser.parse(f)
        expected = {
            'a_num': u'A1878923',
            'addr1': (u'5233 Tiszagyenda Táncsics Mihály út '
                      u'10 4. emelet 10. ajtó'),
            'city': u'Tiszagyenda',
            'house_num': u'10 4 emelet 10 ajtó',
            'mt_id': u'111111111',
            'name1': u'Erdélyiné Fosos Erzsébet',
            'name2': u'Erdélyiné Sipos Erzsébet',
            'phone1': u'306902317',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'Táncsics Mihály út',
            'task_id': u'386',
            'task_type': u'H-Hibrid TV Hibaelhárítás SAT (HSZI SZK) [NG]',
            'ticket_id': u'111111.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'5233'
        }

        self.assertDictEqual(output, expected)

    def test_file4(self):
        f = self._get_mail_file('test4.html')
        output = self.parser.parse(f)
        expected = {
            'a_num': u'K4951471',
            'addr1': u'2030 Érd, Duna utca 64.',
            'city': u'Érd',
            'devices': [
                {'device_sn': u'248837917',
                 'device_type': u'Koax Dual 3.0 Cisco EPC3925'},
            ],
            'house_num': u'64',
            'mt_id': u'804285536',
            'name1': u'Externet Nyrt.',
            'name2': u'Madák Attiláné',
            'phone1': u'703612461',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'Duna utca',
            'task_id': u'695',
            'task_type': u'H-Internet Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'61913775.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'2030'
        }

        self.assertDictEqual(output, expected)

    def test_file5(self):
        f = self._get_mail_file('test5.html')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'HAJDÚSZOBOSZLÓ 4200 Hőforrás utca 27-33.',
            'agreed_time': '',
            'city': u'Hajdúszoboszló',
            'date_created': u'2014-01-30 07:25:05',
            'devices': [
                {'device_card_sn': u'014786985714',
                 'device_sn': u'00595875838'},
            ],
            'efp_num': '',
            'house_num': u'27-33',
            'ki_id': u'1156290',
            'mt_id': u'888888888',
            'name1': u'DIANISKA KFT',
            'phone1': u'309670566',
            'req_type': u'Műszaki Hozzáférés - [LESZ] - SATTV',
            'street': u'Hőforrás utca',
            'task_type': u'L-DVBS eszköz leszerelés díjtartozás miatt [SPA]',
            'ticket_id': u'47025926-270',
            'zip': u'4200'
        }

        self.assertDictEqual(output, expected)

    def test_file6(self):
        f = self._get_mail_file('test6.html')
        output = self.parser.parse(f)
        expected = {
            'a_num': u'ktv8000192174',
            'addr1': u'2013 Pomáz Magyar utca 14 /B',
            'agreed_time': u'2016-07-22 10:00:44 - 2016-07-22 12:00:44',
            'city': u'Pomáz',
            'devices': [
                {'device_sn': u'255865885',
                 'device_type': u'ISB2201_STB'},
                {'device_sn': u'255865856',
                 'device_type': u'ISB2201_STB'},
                {'device_sn': u'255865846',
                 'device_type': u'ISB2201_STB'},
                {'device_sn': u'243416276',
                 'device_type': u'Koax Dual 3.0 Cisco EPC3925'}
            ],
            'house_num': u'14 /B',
            'mt_id': u'460789880',
            'name1': u'Sztankovszkyné Póczik Katalin',
            'name2': u'Sztankovszkyné Póczik Katalin',
            'phone1': u'705564258',
            'req_type': u'ACCESS',
            'sla_h': u'24',
            'street': u'Magyar utca',
            'task_id': u'1046',
            'task_type': u'H-Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'61882245.1',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'2013'
        }

        self.assertDictEqual(output, expected)

    def test_file7(self):
        f = self._get_mail_file('test7.html')
        output = self.parser.parse(f)
        expected = {
            'a_num': u'A1145541',
            'addr1': u'2013 Pomáz József Attila utca 2 A',
            'city': u'Pomáz',
            'devices': [
                {'device_sn': u'254633057',
                 'device_type': u'ISB2201_STB'},
                {'device_sn': u'234808075',
                 'device_type': u'Koax Dual 3.0 Cisco EPC3925'}
            ],
            'house_num': u'2 A',
            'mt_id': u'473689583',
            'name1': u'Fehér István',
            'name2': u'Fehér István',
            'phone1': u'302170552',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'József Attila utca',
            'task_id': u'629',
            'task_type': u'H-IPTV Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'61912083.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'2013'
        }

        self.assertDictEqual(output, expected)

    def test_file8(self):
        f = self._get_mail_file('test8.html')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'BUDAPEST 1136 Balzac utca 50/A. 2. emelet 2. ajtó',
            'agreed_time': u'2016-08-02 14:00:00 - 2016-08-02 16:00:00',
            'city': u'Budapest',
            'date_created': u'2016-07-28 18:37:30',
            'house_num': u'50/A 2 emelet 2 ajtó',
            'mt_id': u'824755686',
            'name1': u'Matiz Gréta',
            'order_num': u'2d373033363436343737323038333931',
            'oss_id': u'824755686',
            'phone1': u'+36205397385',
            'phone2': u'13968303',
            'req_type': u'Mûszaki Hozzáférés - [FEL] - GPON_OPTIKA',
            'street': u'Balzac utca',
            'task_type': (u'L-Vonalépítés (Optikai hálózat) [SPA] '
                          u'L-Helyszíni létesítés (GPON) [SPA]'),
            'task_type_list': [u'L-Vonalépítés (Optikai hálózat) [SPA]',
                               u'L-Helyszíni létesítés (GPON) [SPA]'],
            'ticket_id': u'62059132-322',
            'title': u'Szerelési lap',
            'zip': u'1136'
        }

        self.assertDictEqual(output, expected)

    def test_file9(self):
        f = self._get_mail_file('test9.html')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'2085 PILISVÖRÖSVÁR Madarász Viktor utca 20',
            'city': u'Pilisvörösvár',
            'house_num': u'20',
            'mt_id': u'A0466150',
            'name1': u'Gáli János',
            'name2': u'GÁLI JÁNOS',
            'phone1': u'204214878',
            'street': u'Madarász Viktor utca',
            'task_type': u'H-Internet hibaelhárítás (TMSzK)',
            'ticket_id': u'62107940',
            'title': u'Hibaelhárítás Munkalap',
            'zip': u'2085'
        }

        self.assertDictEqual(output, expected)

    def test_file10(self):
        f = self._get_mail_file('test10.html')
        output = self.parser.parse(f)
        expected = {
            'a_num': '',
            'addr1': u'2011 BUDAKALÁSZ Kökény utca 3234 HRSZ3234',
            'city': u'Budakalász',
            'house_num': u'3234 HRSZ3234',
            'mt_id': u'474152443',
            'name1': u'Küzmös György',
            'name2': u'Küzmös György',
            'phone1': u'204713153',
            'req_type': u'SERVICE',
            'sla_h': u'72',
            'street': u'Kökény utca',
            'task_id': u'505',
            'task_type': u'H-PSTN Hibaelhárítás RÉZ (HSZI SZK) [NG]',
            'ticket_id': u'61959788.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'2011'
        }

        self.assertDictEqual(output, expected)

    def test_file11(self):
        f = self._get_mail_file('test11.html')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'2014 CSOBÁNKA Kossuth Lajos utca 11',
            'city': u'Csobánka',
            'house_num': u'11',
            'mt_id': u'26320053',
            'name1': u'Nyilvános Állomás',
            'name2': u'Dénes György',
            'phone1': u'303914300',
            'street': u'Kossuth Lajos utca',
            'task_type': u'H-Elõfizetõi vonalhiba elhárítás',
            'ticket_id': u'61965963',
            'title': u'Hibaelhárítás Munkalap',
            'zip': u'2014'
        }

        self.assertDictEqual(output, expected)

    def test_file12(self):
        f = self._get_mail_file('test12.html')
        output = self.parser.parse(f)
        expected = {
            'a_num': u'ktv6605788774',
            'addr1': u'2013 Pomáz Vár utca 34',
            'agreed_time': u'2016-07-22 12:00:00 - 2016-07-22 14:00:00',
            'city': u'Pomáz',
            'devices': [
                {'device_sn': u'254426669',
                 'device_type': u'ISB2201_STB'},
                {'device_sn': u'254663756',
                 'device_type': u'ISB2201_STB'},
                {'device_sn': u'243647369',
                 'device_type': u'Koax Dual 3.0 Cisco EPC3925'}],
            'house_num': u'34',
            'mt_id': u'822833190',
            'name1': u'Berger András',
            'name2': u'Berger András',
            'phone1': u'202641416',
            'req_type': u'ACCESS',
            'sla_h': u'24',
            'street': u'Vár utca',
            'task_id': u'990',
            'task_type': u'H-Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'61891278.1',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'2013'
        }

        self.assertDictEqual(output, expected)

    def test_file13(self):
        f = self._get_mail_file('test13.html')
        output = self.parser.parse(f)
        expected = {
            'a_num': u'K3558810',
            'addr1': u'2030 Érd, Fácán köz 15. 1. lph.',
            'city': u'Érd',
            'devices': [
                {'device_sn': u'254234121',
                 'device_type': u'ISB2201_STB'},
                {'device_sn': u'261992998',
                 'device_type': u'Koax Dual 3.0 Cisco EPC3925'}],
            'house_num': u'15 1 lph',
            'mt_id': u'704129541',
            'name1': u'Borka Ferencné',
            'name2': u'Borka Ferencné',
            'phone1': u'305563745',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'Fácán köz',
            'task_id': u'538',
            'task_type': u'H-IPTV Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'61934662.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'2030'
        }

        self.assertDictEqual(output, expected)

    def test_file14(self):
        # Check if the name1 is okay or should have a business rule
        # like "if 'ERROR' in data['name1']"
        f = self._get_mail_file('test14.html')
        output = self.parser.parse(f)
        expected = {
            'a_num': '',
            'addr1': u'1184 BUDAPEST Lakatos út 65 -',
            'agreed_time': u'2016-07-26 09:00:00 - 2016-07-26 12:00:00',
            'city': u'Budapest',
            'house_num': u'65 -',
            'mt_id': u'459737363',
            'name1': u'Gõteborgs Food Zrt',
            'name2': u'Gõteborgs Food Zrt',
            'phone1': u'302413923',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'Lakatos út',
            'task_id': u'593',
            'task_type': u'H-Internet Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'61965852.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'1184'
        }

        self.assertDictEqual(output, expected)

    def test_file15(self):
        f = self._get_mail_file('test15.html')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'NAGYKOVÁCSI 2094 Rákóczi utca 10.',
            'agreed_time': u'2016-07-27 14:00:00 - 2016-07-27 16:00:00',
            'city': u'Nagykovácsi',
            'date_created': u'2016-07-22 12:29:02',
            'house_num': u'10',
            'mt_id': u'473374444',
            'name1': u'Barankai Istvánné',
            'order_num': u'36383533333538323237313533353532',
            'oss_id': u'473374444',
            'phone1': u'+3626355584',
            'phone2': u'26355584',
            'req_type': u'Mûszaki Hozzáférés - [LESZ] - ADSL_TPV_REZ',
            'street': u'Rákóczi utca',
            'task_type': u'L-MDF - Multiservice Point [SPA]',
            'ticket_id': u'61928490-534',
            'title': u'Szerelési lap',
            'zip': u'2094'
        }

        self.assertDictEqual(output, expected)

    def test_file16(self):
        f = self._get_mail_file('test16.html')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'SOLYMÁR 2083 Madár utca 2.',
            'agreed_time': u'2016-07-28 12:00:00 - 2016-07-28 14:00:00',
            'city': u'Solymár',
            'date_created': u'2016-07-25 14:54:27',
            'devices': [{'device_sn': u'00912033306224',
                         'device_type': u'Koax Dual 2.0 Thomson THG540'}],
            'house_num': u'2',
            'mt_id': u'704168455',
            'name1': u'Fürjesné Berliner Éva',
            'order_num': u'34313835363434313637363232303638',
            'oss_id': u'704168455',
            'phone1': u'+36304006868',
            'phone2': u'26630376',
            'req_type': u'Mûszaki Hozzáférés - [FEL] - KOAX',
            'street': u'Madár utca',
            'task_type': (u'L-Helyszíni áthelyezés '
                          u'(KOAX) [SPA]'),
            'ticket_id': u'61974667-745',
            'title': u'Szerelési lap',
            'zip': u'2083'
        }

        self.assertDictEqual(output, expected)

    def test_file17(self):
        f = self._get_mail_file('test17.html')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'REMETESZÕLÕS 2090 Csillag sétány 2.',
            'agreed_time': u'2016-07-28 14:00:00 - 2016-07-28 16:00:00',
            'city': u'Remeteszõlõs',
            'date_created': u'2016-07-27 12:01:11',
            'house_num': u'2',
            'mt_id': u'824723727',
            'name1': u'Gerle János Istvánné',
            'order_num': u'2d323431383738323734373036373938',
            'oss_id': u'824723727',
            'phone1': u'+36204989425',
            'phone2': u'26376679',
            'req_type': u'Mûszaki Hozzáférés - [FEL] - KOAX',
            'street': u'Csillag sétány',
            'task_type': u'L-Helyszíni létesítés (KOAX) [SPA]',
            'ticket_id': u'62022764-367',
            'title': u'Szerelési lap',
            'zip': u'2090'
        }

        self.assertDictEqual(output, expected)

    def test_file18(self):
        f = self._get_mail_file('test18.html')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'BUDAPEST 1132 Visegrádi utca 55-57. FS. emelet 2. ajtó',
            'agreed_time': u'2016-08-01 14:00:00 - 2016-08-01 16:00:00',
            'city': u'Budapest',
            'date_created': u'2016-07-26 14:32:55',
            'house_num': u'55-57 FS emelet 2 ajtó',
            'mt_id': u'468104124',
            'name1': u'Sebestyén Béláné',
            'order_num': u'37373934373932363036373332383433',
            'oss_id': u'468104124',
            'phone1': u'+36301237896',
            'phone2': u'13492370',
            'req_type': u'Mûszaki Hozzáférés - [LESZ] - TPV_REZ',
            'street': u'Visegrádi utca',
            'task_type': (u'L-Vonalépítés - Multiservice Point '
                          u'[SPA] L-MDF - Multiservice Point [SPA]'),
            'task_type_list': [u'L-Vonalépítés - Multiservice Point [SPA]',
                               u'L-MDF - Multiservice Point [SPA]'],
            'ticket_id': u'62002628-452',
            'title': u'Szerelési lap',
            'zip': u'1132'
        }

        self.assertDictEqual(output, expected)

    def test_file19(self):
        f = self._get_mail_file('test19.html')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'2085 PILISVÖRÖSVÁR Madarász Viktor utca 20',
            'city': u'Pilisvörösvár',
            'house_num': u'20',
            'mt_id': u'A0466150',
            'name1': u'Gáli János',
            'name2': u'GÁLI JÁNOS',
            'phone1': u'204214878',
            'street': u'Madarász Viktor utca',
            'task_type': u'H-Internet hibaelhárítás (TMSzK)',
            'ticket_id': u'62107940',
            'title': u'Hibaelhárítás Munkalap',
            'zip': u'2085'
        }

        self.assertDictEqual(output, expected)

    def test_file20(self):
        f = self._get_mail_file('test20.html')
        output = self.parser.parse(f)
        expected = {
            'addr1': u'BUDAPEST 1132 Visegrádi utca 58/B. FE. emelet 3. ajtó',
            'agreed_time': u'2016-08-01 12:00:00 - 2016-08-01 14:00:00',
            'city': u'Budapest',
            'date_created': u'2016-07-26 14:41:22',
            'house_num': u'58/B FE emelet 3 ajtó',
            'mt_id': u'479007861',
            'name1': u'Tóth Tibor',
            'order_num': u'34313631313334363533323434353631',
            'oss_id': u'479007861',
            'phone1': u'+3613208952',
            'phone2': u'13208952',
            'req_type': u'Mûszaki Hozzáférés - [LESZ] - TPV_REZ',
            'street': u'Visegrádi utca',
            'task_type': (u'L-Vonalépítés - Multiservice Point '
                          u'[SPA] L-MDF - Multiservice Point [SPA]'),
            'task_type_list': [u'L-Vonalépítés - Multiservice Point [SPA]',
                               u'L-MDF - Multiservice Point [SPA]'],
            'ticket_id': u'62002879-423',
            'title': u'Szerelési lap',
            'zip': u'1132'
        }

        self.assertDictEqual(output, expected)

    def test_file21(self):
        """
        Test case for numbered street parsing
        """
        f = self._get_mail_file('test21.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'a_num': u'ktv6959169289',
            'addr1': u'1173 Budapest 507. utca 6',
            'city': u'Budapest',
            'devices': [
                {'device_sn': u'EQ131A4005170',
                 'device_type': u'Koax Dual 3.0 D-Link DCM-301'}
            ],
            'house_num': u'6',
            'mt_id': u'492579155',
            'name1': u'Szuhánszky Zsuzsanna',
            'name2': u'Skornyák Ferenc',
            'phone1': u'208011888',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'507. utca',
            'task_id': u'480',
            'task_type': u'H-Internet Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'62192005.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'1173'
        }

        self.assertDictEqual(output, expected)

    def test_file22(self):
        """
        Test case HRSZ, also for having extra colon in the address
        """
        f = self._get_mail_file('test22.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'a_num': u'K3799104',
            'addr1': u'5008 SZOLNOK Karinthy Frigyes út HRSZ:13751/4',
            'city': u'Szolnok',
            'devices': [
                {'device_sn': u'00541313324',
                 'device_type': u'SAGEM DS86 HD DVB-S SET TOP BOX (MT)'},
                {'device_sn': u'00657983796',
                 'device_type': u'Kaon KSF-CO1000 HD HIBRID STB'},
            ],
            'house_num': u'HRSZ:13751/4',
            'mt_id': u'459427702',
            'name1': u'Hasznos Zsuzsa',
            'name2': u'Hasznos Zsuzsa',
            'phone1': u'202652318',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'Karinthy Frigyes út',
            'task_id': u'416',
            'task_type': u'H-DVBS Hibaelhárítás SAT (HSZI SZK) [NG]',
            'ticket_id': u'62289554.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'5008',
        }

        self.assertDictEqual(output, expected)

    def test_file23(self):
        """
        Test case HRSZ, also for having extra colon in the address
        """
        f = self._get_mail_file('test23.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'a_num': u'K3464751',
            'addr1': u'5081 Szajol Széchenyi út 5',
            'city': u'Szajol',
            'devices': [
                {'device_sn': u'X111843091023776',
                 'device_type': u'INTEK HD-S10CX STB'},
                {'device_sn': u'CJZA05928133457',
                 'device_type': u'ADB-5800S -HD AVC DVB-S SET TOP BOX (MT)'},
            ],
            'house_num': u'5',
            'mt_id': u'477931030',
            'name1': u'Balogh István',
            'name2': u'Balogh István',
            'phone1': u'302284276',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'Széchenyi út',
            'task_id': u'420',
            'task_type': u'H-DVBS Hibaelhárítás SAT (HSZI SZK) [NG]',
            'ticket_id': u'62374561.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'5081'
        }

        self.assertDictEqual(output, expected)

    def test_file24(self):
        """
        Test case for "Begyujtendo osszeg" field
        """
        f = self._get_mail_file('test24.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'NAGYKOVÁCSI 2094 Szent Flórián utca 5/B.',
            'agreed_time': u'2016-09-03 10:00:00 - 2016-09-03 12:00:00',
            'city': u'Nagykovácsi',
            'collectable_money': u'8000Ft',
            'date_created': u'2016-08-27 16:04:40',
            'house_num': u'5/B',
            'mt_id': u'825351637',
            'name1': u'Julie Arnold',
            'order_num': u'2d343433343434393336353636313539',
            'oss_id': u'825351637',
            'phone1': u'+36304104835',
            'req_type': u'Mûszaki Hozzáférés - [FEL] - KOAX',
            'street': u'Szent Flórián utca',
            'task_type': u'L-Helyszíni létesítés (KOAX) [SPA]',
            'ticket_id': u'62669581-643',
            'title': u'Szerelési lap',
            'zip': u'2094'
        }

        self.assertDictEqual(output, expected)

    def test_file25(self):
        """
        testing task type duplicate filtering
        """
        f = self._get_mail_file('test25.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'2000 SZENTENDRE Rózsa utca 16',
            'city': u'Szentendre',
            'house_num': u'16',
            'mt_id': u'706576846',
            'name1': u'Mikrofiber Marketing Kft',
            'devices': [
                {'device_sn': u'MENNY-17111482/1/1',
                 'device_type': u'ADSL_1 ADSL ef. MODEM D-Link DSL-360R'},
            ],
            'phone1': u'+36706135717',
            'street': u'Rózsa utca',
            'task_type': (u'L-Vonal + NDSL kiépítése L-MDF bekötés NAKED'),
            'task_type_list': [u'L-Vonal + NDSL kiépítése',
                               u'L-MDF bekötés NAKED'],
            'ticket_id': u'62761843-729',
            'title': u'Munkaelrendelés',
            'zip': u'2000'
        }

        self.assertDictEqual(output, expected)

    def test_file26(self):
        """
        Another test case for "Begyujtendo osszeg" field
        """
        f = self._get_mail_file('test26.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': (u'SZENTENDRE 2000 Széchenyi István tér 8. '
                      u'1. emelet 3. ajtó'),
            'agreed_time': u'2016-09-14 08:00:00 - 2016-09-14 10:00:00',
            'city': u'Szentendre',
            'collectable_money': u'8000Ft',
            'date_created': u'2016-09-10 10:43:21',
            'house_num': u'8 1 emelet 3 ajtó',
            'mt_id': u'825657672',
            'name1': u'Horváth Zsolt',
            'order_num': u'2d323639333337323135383232343239',
            'oss_id': u'825657672',
            'phone1': u'+36306610993',
            'req_type': u'Mûszaki Hozzáférés - [FEL] - ADSL_REZ',
            'street': u'Széchenyi István tér',
            'task_type': (u'L-Vonalépítés [SPA] L-MDF Felszerelés (Host) '
                          u'[SPA] L-Helyszíni létesítés (REZ) [SPA]'),
            'task_type_list': [u'L-Vonalépítés [SPA]',
                               u'L-MDF Felszerelés (Host) [SPA]',
                               u'L-Helyszíni létesítés (REZ) [SPA]'],
            'ticket_id': u'62913946-477',
            'title': u'Szerelési lap',
            'zip': u'2000'
        }

        self.assertDictEqual(output, expected)

    def test_file27(self):
        """
        New format, [KEY = VALUE] parsing test
        """
        f = self._get_mail_file('test27.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'a_num': '',
            'addr1': u'5000 SZOLNOK Vízpart körút 82 -',
            'city': u'Szolnok',
            'devices': [
                {'device_sn': u'00528534570',
                 'device_type': u'HUAWEI EC2208S HD HIBRID STB'},
                {'device_sn': u'00528558830',
                 'device_type': u'HUAWEI EC2208S HD HIBRID STB'},
                {'device_sn': u'00528585435',
                 'device_type': u'HUAWEI EC2218SS HD PVR(320GB)HIBRID STB'}],
            'house_num': u'82 -',
            'mt_id': u'468405707',
            'name1': u'Antal Attila',
            'name2': u'Antal Attila',
            'phone1': u'703190227',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'Vízpart körút',
            'task_id': u'374',
            'task_type': u'H-Hibrid TV Hibaelhárítás SAT (HSZI SZK) [NG]',
            'ticket_id': u'63050769.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'5000',
        }

        self.assertDictEqual(output, expected)

    def test_file28(self):
        f = self._get_mail_file('test28.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'1007 BUDAPEST Hajós Alfréd sétány 2',
            'city': u'Budapest',
            'devices': [{'device_sn': u'MENNY-17114619/1/1',
                         'device_type': u'3PLAY_HGW_1 Speedport Entry 2i'}],
            'house_num': u'2',
            'mt_id': u'462029189',
            'name1': u'Magyar Úszó Szövetség',
            'order_num': u'7275914',
            'phone1': u'+36303386916',
            'street': u'Hajós Alfréd sétány',
            'task_type': u'L-Szolgáltatás üzembehelyezés (Réz)',
            'ticket_id': u'63072441-1014',
            'title': u'Munkaelrendelés',
            'zip': u'1007'
        }

        self.assertDictEqual(output, expected)

    def test_file29(self):
        """ Test ignore devices with empty sn"""
        f = self._get_mail_file('test29.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'TÓSZEG 5091 Vadász utca 11.',
            'agreed_time': u'2016-10-03 16:00:00 - 2016-10-03 18:00:00',
            'city': u'Tószeg',
            'date_created': u'2016-10-01 22:58:46',
            'house_num': u'11',
            'mt_id': u'801137263',
            'name1': u'Harmati Imre',
            'order_num': u'2d313333303039383838313836333037',
            'oss_id': u'801137263',
            'phone1': u'+36306191456',
            'req_type': u'Műszaki Hozzáférés - [FEL] - GPON_OPTIKA',
            'street': u'Vadász utca',
            'task_type': u'L-MDF - Multiservice Point [SPA]',
            'ticket_id': u'63313981-544',
            'title': u'Szerelési lap',
            'zip': u'5091'
        }

        self.assertDictEqual(output, expected)

    def test_file30(self):
        """test processing of multiple tasks with no space for separator"""
        f = self._get_mail_file('test30.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'Tószeg 5091 Vadvirág 1/B.',
            'agreed_time': u'Nincs, vagy lejárt!',
            'city': u'Tószeg',
            'date_created': u'2016-09-12 14:42:28',
            'house_num': u'1/B',
            'mt_id': u'825295282',
            'name1': u'Jakoda-Tóth Andrea',
            'order_num': u'34393836303438373230383432303930',
            'oss_id': u'825295282',
            'phone1': u'205596925',
            'phone2': u'56557198',
            'req_type': u'Műszaki Hozzáférés - [FEL] - GPON_OPTIKA',
            'street': u'Vadvirág',
            'task_type': (u'L-Vonalépítés (Optikai hálózat) [SPA] L-Helyszíni'
                          u' létesítés (GPON) [SPA]'),
            'task_type_list': [u'L-Vonalépítés (Optikai hálózat) [SPA]',
                               u'L-Helyszíni létesítés (GPON) [SPA]'],
            'ticket_id': u'62945323-553',
            'title': u'Szerelési lap',
            'zip': u'5091'
        }

        self.assertDictEqual(output, expected)

    def test_file31(self):
        """new format again"""
        f = self._get_mail_file('test31.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'7630 PÉCS Deák Ferenc utca 37',
            'city': u'Pécs',
            'house_num': u'37',
            'mt_id': u'461998427',
            'name1': u'Fruitica Kft.',
            'order_num': u'7278011',
            'devices': [{'device_sn': u'NE001ARI',
                         'device_type': u'ISDN2_1 IS2 NetMod INTRACOM'}],
            'phone1': u'+36204556932',
            'street': u'Deák Ferenc utca',
            'task_type': (u'L-Szolgáltatás üzembehelyezés (Optika)'
                          u' L-Vonalépítés (Optikai hálózat)'),
            'task_type_list': [u'L-Szolgáltatás üzembehelyezés (Optika)',
                               u'L-Vonalépítés (Optikai hálózat)'],
            'ticket_id': u'63328472-2330',
            'title': u'Munkaelrendelés',
            'zip': u'7630'
        }

        self.assertDictEqual(output, expected)

    def test_file32(self):
        """Test setting MT ID to ticket ID if no MT ID is present"""
        f = self._get_mail_file('test32.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'a_num': u'K3508460',
            'addr1': u'1171 BUDAPEST PESTI ÚT 335',
            'city': u'Budapest',
            'devices': [{'device_sn': u'254069370',
                         'device_type': u'ISB2201_STB'},
                        {'device_sn': u'255361951',
                         'device_type': u'ISB2201_STB'},
                        {'device_sn': u'232014329',
                         'device_type': u'Koax Dual 3.0 Cisco EPC3925'}],
            'house_num': u'335',
            'mt_id': u'63591488.2',
            'name1': u'Jánószki István',
            'name2': u'Jánószki István',
            'phone1': u'209818671',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'PESTI ÚT',
            'task_id': u'585',
            'task_type': u'H-Internet Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'63591488.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'1171'
        }

        self.assertDictEqual(output, expected)

    def test_file33(self):
        """Test setting MT ID to ticket ID if no MT ID is present"""
        f = self._get_mail_file('test33.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'5400 MEZŐTÚR Nyári Nagy Pál utca 17 -',
            'city': u'Mezőtúr',
            'house_num': u'17 -',
            'mt_id': u'63593804.2',
            'name1': u'Zolnai Krisztina',
            'name2': u'Zolnai Krisztina',
            'phone1': u'705881068',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'Nyári Nagy Pál utca',
            'task_id': u'399',
            'task_type': u'H-DVBS Hibaelhárítás SAT (HSZI SZK) [NG]',
            'ticket_id': u'63593804.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'5400',
        }

        self.assertDictEqual(output, expected)

    def test_file34(self):
        """Test setting MT ID to ticket ID if no MT ID is present"""
        f = self._get_mail_file('test34.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'1171 BUDAPEST Gyöngfüzér utca 14 -',
            'city': u'Budapest',
            'house_num': u'14 -',
            'mt_id': u'63593517.2',
            'name1': u'Salamon Imre',
            'name2': u'Salamon Imre',
            'phone1': u'304553480',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'Gyöngfüzér utca',
            'task_id': u'477',
            'task_type': u'H-Internet Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'63593517.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'1171'
        }

        self.assertDictEqual(output, expected)

    def test_file35(self):
        """Test setting MT ID to ticket ID if no MT ID is present"""
        f = self._get_mail_file('test35.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'a_num': u'A2396294',
            'addr1': u'1174 BUDAPEST TÁNCSICS MIHÁLY ÚT 31 -',
            'city': u'Budapest',
            'devices': [{'device_sn': u'G6D03796LRL',
                         'device_type': u'Tatung STB-3112 CDA'},
                        {'device_sn': u'261987941',
                         'device_type': u'Koax Dual 3.0 Cisco EPC3925'}],
            'house_num': u'31 -',
            'mt_id': u'63592472.2',
            'name1': u'Tóth Roland',
            'name2': u'Tóth Roland',
            'phone1': u'303583973',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'TÁNCSICS MIHÁLY ÚT',
            'task_id': u'552',
            'task_type': u'H-IPTV Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'63592472.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'1174'
        }

        self.assertDictEqual(output, expected)

    def test_file36(self):
        """Test setting MT ID to ticket ID if no MT ID is present"""
        f = self._get_mail_file('test36.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'a_num': u'A2441759',
            'addr1': u'1171 BUDAPEST Perec utca 19 .',
            'city': u'Budapest',
            'devices': [{'device_sn': u'G7D0K512LRL',
                         'device_type': u'Tatung STB-3112 CDA'},
                        {'device_sn': u'NQ1606536001304',
                         'device_type': u'Koax Dual 3.0 Sagemcom F@ST3686'}],
            'house_num': u'19',
            'mt_id': u'63591180.2',
            'name1': u'Martincsevics Györgyné',
            'name2': u'Martincsevics Györgyné',
            'phone1': u'703185142',
            'req_type': u'SERVICE',
            'sla_h': u'72',
            'street': u'Perec utca',
            'task_id': u'530',
            'task_type': u'H-VoCA Hibaelhárítás KOAX (HSZI SZK) [NG]',
            'ticket_id': u'63591180.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'1171'
        }

        self.assertDictEqual(output, expected)

    def test_file37(self):
        f = self._get_mail_file('test37.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'2000 SZENTENDRE Dózsa György út 67 FS em. 5 ajtó',
            'city': u'Szentendre',
            'devices': [{'device_sn': u'MENNY-16244276/1/1',
                         'device_type': u'3PLAY_STB_1 KISS STB_160GB'},
                        {'device_sn': u'W42230600002598',
                         'device_type': u'VDSL_HGW_1 SpeedportW721V(hu)'},
                        {'device_sn': u'172541317',
                         'device_type': u'3PLAY_MN_STB_1 ISB2001_STB'},
                        {'device_sn': u'255996257',
                         'device_type': u'3PLAY_MN_STB_2 ISB2201_STB'}],
            'house_num': u'67 FS em 5 ajtó',
            'mt_id': u'469448568',
            'name1': u'Kézdi Miklós Pálné',
            'phone1': u'+36301975740',
            'street': u'Dózsa György út',
            'ticket_id': u'63290978-795',
            'task_type': u'Munkaelrendelés',
            'title': u'Munkaelrendelés',
            'zip': u'2000'}

        self.assertDictEqual(output, expected)

    def test_file38(self):
        f = self._get_mail_file('test38.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'7900 SZIGETVÁR Szabadság utca 43',
            'city': u'Szigetvár',
            'devices': [{'device_sn': u'252819612',
                         'device_type': u'3PLAY_STB_1 ISB6030_STB_HDD_320GB'},
                        {'device_sn': u'MENNY-17090751/1/1',
                         'device_type': u'3PLAY_MN_STB_1 ISB2001_STB'}],
            'house_num': u'43',
            'mt_id': u'823222159',
            'name1': u'Góra Tamás Zsolt',
            'phone1': u'+36309978426',
            'street': u'Szabadság utca',
            'task_type': u'L-Szolgáltatás üzembehelyezés (Optika)',
            'ticket_id': u'63666853-1035',
            'title': u'Munkaelrendelés',
            'zip': u'7900'
        }

        self.assertDictEqual(output, expected)

    def test_file40(self):
        """
        Test when there are multiple sheets on a single email - testing
        extraction of devices mainly
        """
        f = self._get_mail_file('test40.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'TÓSZEG 5091 Tópart út 2.',
            'agreed_time': u'2016-11-07 08:00:00 - 2016-11-07 10:00:00',
            'city': u'Tószeg',
            'date_created': u'2016-11-03 16:46:05',
            'devices': [
                {'device_ownership': u'Bérelt',
                 'device_sn': u'00528552987',
                 'device_type': u'HUAWEI EC2208S HD HIBRID STB'},
                {'device_ownership': u'Bérelt',
                 'device_sn': u'CJZA03919102134',
                 'device_type': u'ADB-5800S -HD AVC DVB-S SET TOP BOX (MT)'},
                {'device_ownership': u'Bérelt',
                 'device_sn': u'CJZA03919102136',
                 'device_type': u'ADB-5800S -HD AVC DVB-S SET TOP BOX (MT)'}],
            'house_num': u'2',
            'mt_id': u'474831361',
            'name1': u'Szabó Józsefné',
            'order_num': u'2d373532363831333136343430333831',
            'oss_id': u'474831361',
            'phone1': u'+36705680851',
            'phone2': u'56431423',
            'req_type': u'Műszaki Hozzáférés - [LESZ] - MSAN_REZ',
            'street': u'Tópart út',
            'task_type': (u'L-Vonalépítés - Multiservice Point [SPA] '
                          u'L-MDF - Multiservice Point [SPA]'),
            'task_type_list': [u'L-Vonalépítés - Multiservice Point [SPA]',
                               u'L-MDF - Multiservice Point [SPA]'],
            'ticket_id': u'63892344-605',
            'title': u'Szerelési lap',
            'zip': u'5091'
        }

        self.assertDictEqual(output, expected)

    def test_file41(self):
        """
        Test when there are multiple sheets on a single email - testing
        extraction of devices mainly
        """
        f = self._get_mail_file('test41.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'TÓSZEG 5091 Széchenyi út 33.',
            'agreed_time': u'2016-11-07 12:00:00 - 2016-11-07 14:00:00',
            'city': u'Tószeg',
            'date_created': u'2016-11-04 08:18:21',
            'devices': [
                {'device_ownership': u'Bérelt',
                 'device_sn': u'ZTEEF01BB410680',
                 'device_type': u'ZXV10 H201L'}],
            'house_num': u'33',
            'mt_id': u'706215345',
            'name1': u'Szabó Anita',
            'order_num': u'37313335323737333532313939343036',
            'oss_id': u'706215345',
            'phone1': u'+36706658716',
            'phone2': u'56402818',
            'req_type': u'Műszaki Hozzáférés - [LESZ] - ADSL_REZ',
            'street': u'Széchenyi út',
            'task_type': (u'L-Vonalépítés - Multiservice Point [SPA] '
                          u'L-MDF - Multiservice Point [SPA]'),
            'task_type_list': [u'L-Vonalépítés - Multiservice Point [SPA]',
                               u'L-MDF - Multiservice Point [SPA]'],
            'ticket_id': u'63901830-481',
            'title': u'Szerelési lap',
            'zip': u'5091'
        }

        self.assertDictEqual(output, expected)

    def test_file42(self):
        """
        Test extracting devices and data with multiple <html> tags in the
        document. Sweet
        """
        f = self._get_mail_file('test42.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'addr1': u'ÚJSZÁSZ 5052 Jókai út 16.',
            'agreed_time': u'2016-11-07 15:00:00 - 2016-11-07 17:00:00',
            'city': u'Újszász',
            'date_created': u'2016-11-03 09:20:05',
            'devices': [
                {'device_ownership': u'Bérelt',
                 'device_sn': u'00595751190',
                 'device_type': u'INTEK-S50CX DVB-S2 MPEG4 SD SET TOP BOX'},
                {'device_ownership': u'Bérelt',
                 'device_sn': u'00595872636',
                 'device_type': u'INTEK-S50CX DVB-S2 MPEG4 SD SET TOP BOX'},
                {'device_sn': u'ZTEEF01DBJ00545',
                 'device_type': u'ZXV10 H201L BJ'}],
            'house_num': u'16',
            'mt_id': u'691313039',
            'name1': u'Korona Attila',
            'order_num': u'35353533353131303737373031333533',
            'oss_id': u'691313039',
            'phone1': u'+36703492323',
            'phone2': u'56950615',
            'req_type': u'Műszaki Hozzáférés - [MÓD] - ADSL_REZ',
            'street': u'Jókai út',
            'task_type': u'L-Helyszíni Feladat MULTI-DVBS [SPA]',
            'ticket_id': u'63878315-490',
            'title': u'Szerelési lap',
            'zip': u'5052'
        }

        self.assertDictEqual(output, expected)

    def test_file43(self):
        """
        Test extracting devices and data with multiple <html> tags in the
        document. Sweet
        """
        f = self._get_mail_file('test43.html')
        output = self.parser.parse(f)
        # PPrinter(indent=0).pprint(output)
        expected = {
            'a_num': u'K3621277',
            'addr1': u'5000 Szolnok Kert utca 32',
            'city': u'Szolnok',
            'devices': [
                {'device_sn': u'CJZA03919102559',
                 'device_type': u'ADB-5800S -HD AVC DVB-S SET TOP BOX (MT)'},
                {'device_sn': u'CJZA03919102560',
                 'device_type': u'ADB-5800S -HD AVC DVB-S SET TOP BOX (MT)'},
                {'device_sn': u'CJZA03919102562',
                 'device_type': u'ADB-5800S -HD AVC DVB-S SET TOP BOX (MT)'}],
            'house_num': u'32',
            'mt_id': u'482898501',
            'name1': u'Táncosné Volter Mária',
            'name2': u'Táncos László',
            'phone1': u'203976402',
            'req_type': u'SERVICE',
            'sla_h': u'24',
            'street': u'Kert utca',
            'task_id': u'785',
            'task_type': u'H-DVBS Hibaelhárítás SAT (HSZI SZK) [NG]',
            'ticket_id': u'63867244.2',
            'title': u'Hibaelhárítási munkalap',
            'zip': u'5000'
        }

        self.assertDictEqual(output, expected)


if __name__ == '__main__':
    unittest.main()

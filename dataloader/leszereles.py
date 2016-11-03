# -*- coding: utf-8 -*-

import datetime

from base import DataLoaderBase, NULL
from processors.field_map import Fields


class Leszereles(DataLoaderBase):

    class AlreadyExistsError(Exception):
        pass

    def _post_init(self):
        self._db = self.LESZ_DB

    def insert_mail_data(self, data, mail):
        if Fields.DEVICES in data:
            loc_id = self._get_loc_id(data)
            default_mech_id = self._get_default_mech_id()
            try:
                client_id = self._insert_data(data, loc_id, default_mech_id)
            except self.AlreadyExistsError:
                return None
            self._insert_devices(data, client_id)
            # self._insert_mail_content(client_id, mail.html)

    def _insert_devices(self, data, client_id):
        stmt = ('INSERT dbo.BoxKartyak'
                '(bk_uAzon, Box, Kartya, bkTulajdonlas,'
                'Vart_Box, Vart_Kartya)'
                'VALUES (%s,%s,%s,%s,%s,%s)')

        conn = self._connect_db(self._db)

        for device in data[Fields.DEVICES]:
            cursor = conn.cursor()
            cursor.execute('SELECT count(1) FROM dbo.BoxKartyak '
                           'WHERE bk_uAzon=%s AND Box=%s',
                           (client_id,
                            device[Fields.DEV_SN],))
            num_devices = int(cursor.fetchone()[0])
            if num_devices:
                continue

            params = (
                client_id,
                device[Fields.DEV_SN],
                device.get(Fields.DEV_CARD_SN, NULL),
                '1',
                '0',
                '0',
            )
            cursor.execute(stmt, params)

        conn.commit()
        conn.close()

    def _insert_data(self, data, loc_id, default_mech_id):
        stmt = ('INSERT dbo.Ugyfelek (uNev, MtAzon, u_tAzon, Utca, HazSzam,'
                'Felvitel, Kiadva, Lezarva, u_szAzon, uMegjegyzes, '
                'ugyf_jeloles, Telszam, FromEventus)'
                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')

        conn = self._connect_db(self._db)
        cursor = conn.cursor()

        cursor.execute("SELECT uAzon FROM Ugyfelek WHERE MtAzon=%s AND uNev<>%s"
                       "".format(data[Fields.MT_ID], 'NINCS ADAT'))
        try:
            mt_id = cursor.fetchone()[0]
            if mt_id:
                return mt_id
        except:
            pass

        try:
            params = (
                data[Fields.NAME1],
                data[Fields.MT_ID] + 'b',
                loc_id,
                data[Fields.STREET],
                data[Fields.HOUSE_NUM],
                datetime.datetime.now(),
                datetime.datetime.now(),
                datetime.datetime.now(),
                default_mech_id,
                data.get(Fields.REMARKS, NULL),
                NULL,
                data[Fields.PHONE1],
                '0',
            )
        except KeyError as e:
            raise Exception('Hianyzo adat a feldolgozashoz: {}'.format(e))

        cursor.execute(stmt, params)
        conn.commit()
        cursor.execute('SELECT @@IDENTITY')
        res = cursor.fetchone()[0]
        conn.close()
        return res

    def update_phone_number(self, mt_id, phone_num_str):
        stmt = ('UPDATE dbo.Ugyfelek SET Telszam=%s WHERE MtAzon=%s')
        conn = self._connect_db(self._db)
        cursor = conn.cursor()
        params = (phone_num_str, mt_id)
        cursor.execute(stmt, params)
        conn.commit()
        conn.close()

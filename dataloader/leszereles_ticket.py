# -*- coding: utf-8 -*-

import datetime

from base import NULL, DuplicateItemError
from leszereles import Leszereles
from processors.field_map import Fields


class LeszerelesTicket(Leszereles):

    def insert_mail_data(self, data, mail):
        loc_id = self._get_loc_id(data)
        default_mech_id = self._get_default_mech_id()
        try:
            client_id = self._insert_data(data, loc_id, default_mech_id, mail.html)
        except self.AlreadyExistsError:
            return None
        self._insert_devices(data, client_id)
        self._insert_mail_content(client_id, mail.html)

    def _insert_data(self, data, loc_id, default_mech_id, mail_content):
        stmt = ('INSERT dbo.Ugyfelek (uNev, MtAzon, u_tAzon, Utca, HazSzam,'
                'Felvitel, Kiadva, Lezarva, u_szAzon, uMegjegyzes, '
                'ugyf_jeloles, Telszam, FromEventus, JegyAzon)'
                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')

        conn = self._connect_db(self._db)
        cursor = conn.cursor()

        cursor.execute("SELECT uAzon FROM Ugyfelek WHERE JegyAzon='{}'"
                       "".format(data[Fields.TICKET_ID]))
        client_id = cursor.fetchone()
        if client_id:
            # Fix missing ticket from database
            cursor.execute('SELECT COUNT(1) dbo.ugyfelek_mail'
                           'WHERE um_uAzon={}'.format(client_id[0]))
            mail_present = cursor.fetchone()
            if not mail_present:
                self._insert_mail_content(client_id[0], mail_content)

            raise DuplicateItemError(u'A {} jegy azonosító már bent van az '
                                     u'adatbázisban'
                                     u''.format(data[Fields.TICKET_ID]))

        cursor.execute("SELECT COUNT(1) FROM Ugyfelek WHERE MtAzon like '{}%%'"
                       "".format(data[Fields.MT_ID]))
        mt_count = cursor.fetchone()[0]
        mt_postfix = 'X' * mt_count

        try:
            params = (
                data[Fields.NAME1],
                data[Fields.MT_ID] + mt_postfix,
                loc_id,
                data[Fields.STREET],
                data[Fields.HOUSE_NUM],
                data.get(Fields.DATE_CREATED, datetime.datetime.now()),
                NULL,
                NULL,
                default_mech_id,
                data.get(Fields.REMARKS, NULL),
                NULL,
                data[Fields.PHONE1],
                '1',
                data[Fields.TICKET_ID],
            )
        except KeyError as e:
            raise Exception('Hianyzo adat a feldolgozashoz: {}'.format(e))

        cursor.execute(stmt, params)
        conn.commit()
        cursor.execute('SELECT @@IDENTITY')
        res = cursor.fetchone()[0]
        conn.close()
        return res

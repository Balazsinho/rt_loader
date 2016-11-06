# -*- coding: utf-8 -*-

from unidecode import unidecode

from base import DataLoaderBase, NULL, DuplicateItemError
from processors.field_map import Fields


class Nyilvantarto(DataLoaderBase):

    def _post_init(self):
        self._db = self.NYILV_DB

    def insert_mail_data(self, data, mail):
        loc_id = self._get_loc_id(data)
        default_mech_id = self._get_default_mech_id()
        try:
            client_type_id = self._get_client_type_id(data)
        except Exception as e:
            self.logger.error(e)
            client_type_id = None
        new_id = self._insert_data(data, loc_id, default_mech_id,
                                   client_type_id, mail.mail_date)
        self._insert_mail_content(new_id, mail.pretty)

    def _get_client_type_id(self, data):
        conn = self._connect_db(self._db)
        try:
            task_type = data.get(Fields.TASK_TYPE) or data.get(Fields.TITLE)
        except Exception:
            # Handle missing task type
            raise Exception('Nem talaltam ugyfeltipust a dokumentumban')
        cursor = conn.cursor()
        cursor.execute(u'SELECT utAzon, utNev FROM UgyfelTipus WHERE torolt=0')

        client_type_id = None
        res = cursor.fetchone()
        while res:
            if unidecode(res[1]) == unidecode(task_type):
                client_type_id = res[0]
                break
            res = cursor.fetchone()

        if not client_type_id:
            self.logger.warning(u'Ismeretlen UgyfelTipus: {}'
                                ''.format(task_type))
            cursor.execute('INSERT dbo.UgyfelTipus (utNev, Torolt)'
                           'VALUES (%s,%s)', (task_type, False))
            cursor.execute('SELECT @@IDENTITY')
            client_type_id = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        return client_type_id

    def _insert_data(self, data, loc_id, default_mech_id,
                     client_type_id, mail_date):
        stmt = ('INSERT dbo.Ugyfelek (uNev, MtAzon, u_tAzon, Utca, HazSzam,'
                'Felvitel, Kiadva, Lezarva, u_szAzon, u_utAzon, uMegjegyzes,'
                'JegyAzon) '
                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')

        conn = self._connect_db(self._db)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(1) FROM Ugyfelek WHERE JegyAzon='{}'"
                       "".format(data[Fields.TICKET_ID]))
        mt_count = cursor.fetchone()[0]
        if mt_count > 0:
            raise DuplicateItemError(u'A {} jegy azonosító már bent van az '
                                     u'adatbázisban'
                                     u''.format(data[Fields.TICKET_ID]))

        # xxx... hack
        cursor.execute("SELECT COUNT(1) FROM Ugyfelek WHERE MtAzon like '{}%%'"
                       "".format(data[Fields.MT_ID]))
        mt_count = cursor.fetchone()[0]
        mt_postfix = 'z' * mt_count

        try:
            params = (
                data[Fields.NAME1],
                data[Fields.MT_ID] + mt_postfix,
                loc_id,
                data[Fields.STREET],
                data[Fields.HOUSE_NUM] +
                (' (BE {})'.format(data[Fields.COLLECTABLE_MONEY]) if
                 Fields.COLLECTABLE_MONEY in data else ''),
                mail_date,
                NULL,
                NULL,
                default_mech_id,
                client_type_id,
                data.get(Fields.REMARKS, NULL),
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

# -*- coding: utf-8 -*-

import pymssql
from processors.field_map import Fields

NULL = None


class DuplicateItemError(Exception):
    pass


class DataLoaderBase(object):

    COMMON_DB = 'CommonFGY'
    NYILV_DB = 'Nyilvantarto'
    LESZ_DB = 'Leszereles'

    def __init__(self, logger, db):
        self.logger = logger
        self._server = db['server']
        self._port = db['port']
        self._user = db['user']
        self._pwd = db['pass']
        self._post_init()

    def _post_init(self):
        pass

    def insert_mail_data(self, data, mail_content):
        raise NotImplementedError()

    def _connect_db(self, db, charset='UTF-8', as_dict=False):
        return pymssql.connect(server=self._server, port=self._port,
                               user=self._user, password=self._pwd,
                               database=db, charset=charset, as_dict=as_dict)

    def _get_default_mech_id(self):
        conn = self._connect_db(self.COMMON_DB)
        cursor = conn.cursor()
        cursor.execute('SELECT TOP 1 szazon FROM szerelok '
                       'WHERE torolt=0 AND alapert=1')
        res = cursor.fetchone()
        conn.close()
        if not res:
            raise Exception('Nincs alapert. szerelo')
        return res[0]

    def _get_loc_id(self, data):
        conn = self._connect_db(self.COMMON_DB)
        zip_code = data[Fields.ZIP]
        cursor = conn.cursor()
        cursor.execute('SELECT tAzon FROM dbo.Telepules WHERE tIrsz={}'
                       ''.format(zip_code))
        res = cursor.fetchone()
        conn.close()
        if not res:
            raise Exception('Ismeretlen varos!')
        return res[0]

    def _insert_data(self, *args, **kwargs):
        raise NotImplementedError()

    def _insert_mail_content(self, client_id, mail_content):
        conn = self._connect_db(self._db)
        cursor = conn.cursor()
        cursor.execute('INSERT dbo.ugyfelek_mail (um_uAzon, umHtml)'
                       'VALUES (%s, %s)', (client_id, mail_content))
        conn.commit()
        conn.close()

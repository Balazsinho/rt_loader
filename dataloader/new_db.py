# -*- coding: utf-8 -*-

import json
import urllib2
import base64

import settings
from base import DuplicateItemError
from processors.field_map import Fields


class NewDb(object):
    def __init__(self, logger):
        self._logger = logger

    def insert_mail_data(self, data, mail):
        url = 'http://{}/api/v1/ticket/create'.format(settings.ROVIDTAV_SERVER)
        auth = base64.encodestring(settings.ROVIDTAV_AUTH).strip()
        auth_header = 'Basic {}'.format(auth)
        data['html'] = mail.pretty
        data['mail_date'] = str(mail.mail_date)
        data['attachments'] = mail.attachments
        req = urllib2.Request(url, json.dumps(data),
                              {'Content-Type': 'application/json'})
        req.add_header('Authorization', auth_header)
        f = urllib2.urlopen(req)
        result = f.read()
        f.close()
        result = json.loads(result)
        if 'error' in result:
            if str(result['error']).startswith('duplicate ticket'):
                raise DuplicateItemError(u'A {} jegy azonosító már bent van az'
                                         u' adatbázisban'
                                         u''.format(data[Fields.TICKET_ID]))
            else:
                raise Exception(u'Hiba a feltöltésben: {}'
                                u''.format(json.dumps(result)))
        return result

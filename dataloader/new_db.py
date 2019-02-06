# -*- coding: utf-8 -*-

import json
import urllib2
import base64

import settings
from base import DuplicateItemError, MissingItemError
from processors.field_map import Fields


class NewDb(object):

    API_VERSION = 1
    TICKET_ENDPOINT = 'ticket/create'
    ATTACHMENT_ENDPOINT = 'ticket/attachment'

    def __init__(self, logger):
        self._logger = logger

    def _do_request(self, endpoint, data, callback=json.loads):
        """
        Returns an authenticated request object for the desired endpoint
        """

        url = 'http://{}/api/v{}/{}'.format(settings.ROVIDTAV_SERVER,
                                            self.API_VERSION,
                                            endpoint)
        auth = base64.encodestring(settings.ROVIDTAV_AUTH).strip()
        auth_header = 'Basic {}'.format(auth)

        try:
            json_data = json.dumps(data)
        except UnicodeDecodeError:
            json_data = json.dumps(data, encoding='latin1')

        req = urllib2.Request(url, json_data,
                              {'Content-Type': 'application/json'})
        req.add_header('Authorization', auth_header)
        f = urllib2.urlopen(req)
        result = callback(f.read()) if callback else f.read()
        f.close()
        return result

    def insert_mail_data(self, data, mail):
        data['html'] = mail.pretty
        data['mail_date'] = str(mail.mail_date)
        data['attachments'] = mail.attachments
        result = self._do_request(self.TICKET_ENDPOINT, data)
        if 'error' in result:
            if str(result['error']).startswith('duplicate ticket'):
                raise DuplicateItemError(u'A {} jegy azonosító már bent van az'
                                         u' adatbázisban'
                                         u''.format(data[Fields.TICKET_ID]))
            else:
                raise Exception(u'Hiba a feltöltésben: {}'
                                u''.format(json.dumps(result)))
        return result

    def upload_attachment(self, data):
        result = self._do_request(self.ATTACHMENT_ENDPOINT, data)
        if 'error' in result:
            if str(result['error']).endswith('does not exist'):
                raise MissingItemError(u'A {} jegy azonosító nem található'
                                       u' adatbázisban'
                                       u''.format(data[Fields.TICKET_ID]))
            else:
                raise Exception(u'Hiba a feltöltésben: {}'
                                u''.format(json.dumps(result)))
        return result

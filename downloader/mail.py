# -*- coding: utf-8 -*-

import random
import string
import re
import time
import email
import email.utils
from datetime import datetime

from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError


class Mail(object):

    ENCODING_META = '<meta charset="utf-8"/>'
    FN_PREFIX = datetime.now().strftime('%Y%m%d_%H%M%S')

    OK = u'OK'
    ERROR = u'HIBA'
    NOTPROC = u'NEM FELDOLGOZHATÓ'
    DUPLICATE = u'DUPLIKÁLT'

    def __init__(self, raw, idx, filename=None):
        self.filename = filename or u'{}_{}.html'.format(self.FN_PREFIX, idx)
        self.idx = idx
        self._date = None
        self.status = self.OK

        self.mail = email.message_from_string('\n'.join(raw))
        payload = self.mail.get_payload()
        if type(payload) in (str, unicode):
            pl = payload
            self.attachments = {}
        else:
            pl = payload[0].get_payload()
            self.attachments = self._parse_attachments()

        self.content = pl
        self.html = pl if self._validate_html(pl) else None
        try:
            self.soup = BeautifulSoup(self.html, 'html.parser') if self.html \
                else None
        except HTMLParseError:
            self.soup = None

    def _validate_html(self, html):
        return '<html' in html

    @property
    def pretty(self):
        return (self.ENCODING_META + self.soup.prettify()) if self.soup else \
            self.content

    @property
    def mail_from(self):
        return self.mail['From'] or self.mail['from']

    @property
    def mail_date(self):
        if not self._date:
            try:
                d = time.mktime(email.utils.parsedate(self.mail['date']))
                self._date = datetime.fromtimestamp(d)
            except Exception:
                self._date = datetime.now()
        return self._date

    def _parse_attachments(self):
        payload = self.mail.get_payload()
        attachments = {}
        if len(payload) > 1:
            for att in payload[1:]:
                att_name = self._get_attachment_name(att)
                payload = att.get_payload()
                if type(payload) == list:
                    try:
                        payload = ''.join(payload)
                    except Exception as e:
                        # Weird attachment, we skip these for now
                        # Debugging shows these are messages as an attachment
                        continue
                attachments[att_name] = payload.replace('\n', '')
        return attachments

    def _get_attachment_name(self, msg):
        """
        Filters out all the content types we don't care for attachments, e.g.
        application/zip, text/html, ...
        """
        att_name = msg['Content-ID']
        if not att_name:
            m = re.search('name=(.*)', msg['Content-Type'] or '', re.I)
            if m:
                att_name = m.group(1)
            else:
                att_name = 'NONAME_' + ''.join(random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(5))
        return att_name.strip('<> "')

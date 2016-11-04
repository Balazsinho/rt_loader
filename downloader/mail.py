# -*- coding: utf-8 -*-

import re
from datetime import datetime


class Mail(object):

    ENCODING_META = '<meta charset="utf-8"/>'
    FN_PREFIX = datetime.now().strftime('%Y%m%d_%H%M%S')

    OK = u'OK'
    ERROR = u'HIBA'
    NOTPROC = u'NEM FELDOLGOZHATÓ'
    DUPLICATE = u'DUPLIKÁLT'

    def __init__(self, raw, idx, filename=None):
        self.raw = raw
        self.idx = idx
        self.filename = filename or '{}_{}.html'.format(self.FN_PREFIX,
                                                        self.idx)
        self._from = None
        self._date = None
        self._html = None
        self._attachments = {}
        self.status = self.OK

        if type(raw) in (unicode, str):
            self._html = raw

    @property
    def html(self):
        return self.ENCODING_META + self._html if self._html \
            else self._parse_html()

    @property
    def mail_from(self):
        if not self._from:
            self._from = self._extract_line('from:', 'From:.*<(?P<data>.*)>')
        return self._from

    @property
    def mail_date(self):
        if not self._date:
            try:
                d = self._extract_line('date:')
                self._date = datetime.strptime(d, '%a, %d %b %Y %H:%M:%S +0200')
            except Exception:
                self._date = datetime.now()
        return self._date

    @property
    def attachments(self):
        if not self._attachments:
            self._parse_attachments()
        return self._attachments

    @attachments.setter
    def attachments(self, att):
        self._attachments = att

    def _parse_attachments(self):
        for line_num, line in enumerate(self.raw):
            if line.lower().startswith('content-disposition'):
                extract_re = ('content-disposition:\s*(?P<disposition>.*);'
                              '\s*filename=(?P<filename>.*)')
                m = re.match(extract_re, line + self.raw[line_num+1], re.I)
                if m and m.group('disposition').strip().lower() in ('attachment', 'inline'):
                    self._attachments[m.group('filename').strip().strip('"')] = \
                        self._extract_attachment(line_num)

    def _extract_attachment(self, line_num):
        attachment_str = ''
        in_attachment = False
        for line in self.raw[line_num:]:
            if re.match('^(\s*|^--.*)$', line):
                if in_attachment:
                    break
                in_attachment = True
            elif in_attachment:
                attachment_str += line.strip()
        return attachment_str

    def _parse_html(self):
        in_html = False
        html_assembled = u''
        for line in self.raw:
            if not in_html:
                if re.search('^<html', line, re.I):
                    in_html = True
                else:
                    continue
            # print chardet.detect(line)
            line = line.decode('ISO-8859-2')
            html_assembled += line.rstrip(u'=')
            if re.search('</html>$', line, re.I):
                break

        # We prefix the HTML text with an encoding meta tag so that it
        # displays properly in the browser
        self._html = self._fix_text(html_assembled).encode('utf-8')
        return self.ENCODING_META + self._html if self._html else ''

    def _extract_line(self, line_start, search_re=None):

        """
        Extracts the data from the lines in the email. It checks for line_start
        for speed, if a regexp is provided, it'll match the line with regexp
        and extract the group named "data" if there's a match
        """

        for line in self.raw:
            if line.lower().startswith(line_start):
                if search_re and re.search(search_re, line, re.I):
                    return self._fix_text(
                        re.search(search_re, line, re.I).group('data'))
                else:
                    return self._fix_text(line[len(line_start):].strip())

        return None

    def _fix_text(self, text):
        """
        The downloaded emails are in latin-2 encoding but having
        =E9, =F5 and friends for special characters.
        This snippet fixes that, i didn't find an implicit method.
        The text itself comes out as ascii, thus the encoding converter
        does not recornize there are something to encode.
        """
        encoding_fixed = u''
        char_iterator = enumerate(text)
        for idx, c in char_iterator:
            if c == '=' and re.match('=[0-9A-F][0-9A-F]',
                                     text[idx:idx+3]):
                ch = unichr(ord(text[idx+1:idx+3].decode('hex')))
                encoding_fixed += ch
                # Jump 2 characters, we just compressed them
                next(char_iterator)
                next(char_iterator)
            else:
                encoding_fixed += c

        return encoding_fixed

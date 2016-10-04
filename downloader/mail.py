import re
import datetime


class Mail(object):

    ENCODING_META = '<meta charset="utf-8"/>'
    FN_PREFIX = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    def __init__(self, raw_lines, idx):
        self.raw = raw_lines
        self.idx = idx
        self.filename = '{}_{}.html'.format(self.FN_PREFIX, self.idx)
        self._from = None
        self._html = None

    @property
    def html(self):
        return self.ENCODING_META + self._html if self._html \
            else self._parse_html()

    @property
    def mail_from(self):
        return self._from or self._parse_from()

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

    def _parse_from(self):
        for line in self.raw:
            if line.lower().startswith('from'):
                w_brackets = re.search('From:.*<(.*)>', line)
                if w_brackets:
                    self._from = w_brackets.group(1)
                else:
                    self._from = self._fix_text(line[5:].strip())
                return self._from

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

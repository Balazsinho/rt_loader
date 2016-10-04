# -*- coding: utf-8 -*-

import poplib
from settings import EMAIL_ACCS
from .mail import Mail


class Downloader(object):

    def __init__(self, logger):
        self.logger = logger

    def _get_account(self, account_key):
        try:
            return EMAIL_ACCS[account_key]
        except KeyError:
            raise Exception('Nem letezo fiok: "{}"!'
                            ''.format(account_key))

    def _get_msg_idxs(self, conn):
        """
        The list returned by the pop3 server looks like
        ['1 14432', '2 7523', ...]
        First number is the index on the server, the second number is the
        octets for the message. We extract the first numbers from here
        to use the correct indexes when doing any processing
        """
        list_cmd = conn.list()
        self.logger.debug('Lista valasz: {}'.format(str(list_cmd)))
        msg_idxs = [int(idx.split()[0]) for idx in list_cmd[1]]
        return reversed(msg_idxs)

    def fetch_mails(self, account_key):
        self.logger.info('Emailek kiolvasasa a kovetkezohoz: "{}"'
                         ''.format(account_key))
        acc = self._get_account(account_key)

        conn = poplib.POP3(acc['host'], acc['port'])
        conn.user(acc['user'])
        conn.pass_(acc['passwd'])

        msg_idxs = self._get_msg_idxs(conn)
        self.logger.debug('Indexek: {}'.format(str(msg_idxs)))
        for msg_idx in msg_idxs:
            try:
                (server_msg, body, _) = conn.retr(msg_idx)
            except Exception as e:
                self.logger.error('Sikertelen letoltes! Index: {}, Hiba: {}'
                                  ''.format(msg_idx, e))
                continue
            else:
                self.logger.debug('Szerver uzenet az emailhez: {}'
                                  ''.format(server_msg))

            yield Mail(body, msg_idx)

        conn.quit()

    def delete_mails(self, account_key, idxs):
        acc = self._get_account(account_key)
        conn = poplib.POP3(acc['host'], acc['port'])
        conn.user(acc['user'])
        conn.pass_(acc['passwd'])
        for msg_idx in idxs:
            try:
                conn.dele(msg_idx)
            except Exception as e:
                self.logger.error('Torles sikertelen. Index: {} Hiba: {}'
                                  ''.format(msg_idx, e))
        conn.quit()

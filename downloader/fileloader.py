# -*- coding: utf-8 -*-

import os
import codecs
import datetime
from utils import create_and_list_dir

from .mail import Mail


class FileLoader(object):

    def __init__(self, logger):
        self.logger = logger
        self._mail_prefix = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self._mail_idxs = {}

    def fetch_mails(self, directory):
        msg_files = create_and_list_dir(self.logger, directory)
        msgs = (codecs.open(f).read() for f in msg_files)

        for idx, msg in enumerate(msgs):
            yield Mail(msg, idx)

    def delete_mails(self, directory, idxs):
        msg_files = create_and_list_dir(self.logger, directory)
        [os.remove(f) for idx, f in enumerate(msg_files) if idx in idxs]

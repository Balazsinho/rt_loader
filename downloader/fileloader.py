# -*- coding: utf-8 -*-

import os
import codecs
from utils import create_and_list_dir

from .mail import Mail


class FileLoader(object):

    def __init__(self, logger):
        self.logger = logger
        self._mail_idxs = {}

    def fetch_mails(self, directory):
        msg_files = create_and_list_dir(self.logger, directory)

        for idx, full_path in enumerate(msg_files):
            filename = os.path.basename(full_path)
            content = codecs.open(full_path).read()
            yield Mail(content, idx, filename)

    def delete_mails(self, directory, idxs):
        msg_files = create_and_list_dir(self.logger, directory)
        [os.remove(f) for idx, f in enumerate(msg_files) if idx in idxs]

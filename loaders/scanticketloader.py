# -*- coding: utf-8 -*-

import codecs
import os
import base64

from loaders.base import (LoaderBase, LoaderException,
                          ErrorsDuringProcess)
from dataloader.base import MissingItemError
from processors.ticketscanparser import TicketScanParser
from processors.field_const import Fields
from utils import create_and_list_dir
from settings import LOADERS, SCAN_DIR


class ScanTicketLoader(LoaderBase):

    # Configuration
    MAX_DOCUMENT_PAGES = 3

    def __init__(self, logger, args):
        super(ScanTicketLoader, self).__init__(logger, args)

    def pre_run(self):
        super(ScanTicketLoader, self).pre_run()
        self.parser = TicketScanParser(self.logger)
        self.dataloaders = []
        for loader_cls_name in LOADERS['scan']:
            loader_module = __import__('dataloader')
            cls = getattr(loader_module, loader_cls_name)
            self.dataloaders.append(cls(self.logger))

    def run(self):
        msg_files = create_and_list_dir(self.logger, SCAN_DIR)

        for full_path in msg_files:
            path, filename = os.path.split(full_path)
            with codecs.open(full_path) as raw_file:
                if filename.startswith('hiba_'):
                    self.logger.info('Fajl atugrasa: {}')
                task_nr, _ = self.parser.task_nr_from_raw(raw_file)
                raw_file.seek(0)
                raw_data = raw_file.read()

            if not task_nr:
                self.logger.error('Nem talaltam WFMS azonositot: {}'
                                  ''.format(full_path))
                os.rename(full_path, os.path.join(path, 'hiba_' + filename))
                continue

            data = {
                Fields.TICKET_ID: task_nr,
                'attachment_name': filename,
                'attachment_content': base64.b64encode(raw_data),
            }

            uploaded = False
            for l in self.dataloaders:
                try:
                    l.upload_attachment(data)
                    uploaded = True
                except MissingItemError:
                    self.logger.warning('Nincs ilyen jegy: {}'
                                        ''.format(task_nr))
                except Exception as e:
                    self.logger.error('Hiba a feltoltes ({}) soran: {}'
                                      ''.format(task_nr, e))

            if uploaded:
                try:
                    os.remove(full_path)
                except Exception as e:
                    self.logger.error('Hiba a torles ({}) soran: {}'
                                      ''.format(task_nr, e))

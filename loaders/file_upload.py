# -*- coding: utf-8 -*-

import settings
from downloader.fileloader import FileLoader
from processors.mailparser import MailParser
from dataloader.nyilvantarto import Nyilvantarto  # @UnusedImport
from dataloader.leszereles import Leszereles  # @UnusedImport
from dataloader.new_db import NewDb  # @UnusedImporT
from dataloader.new_db_uninst import NewDbUninst  # @UnusedImporT

from munka import MunkaLoader

from settings import LOADERS


class FileUpload(MunkaLoader):

    """
    Uploads and deletes the files stored in settings.MAIL_UPLOAD_DIR
    """

    def pre_run(self):
        self.email_acc = settings.MAIL_UPLOAD_DIR
        self.downloader = FileLoader(self.logger)
        self.parser = MailParser(self.logger)
        self.dataloaders = []
        for loader_cls_name in LOADERS['fileupload']:
            loader_module = __import__('dataloader')
            cls = getattr(loader_module, loader_cls_name)
            self.dataloaders.append(cls(self.logger))

    def _duplicate(self, *args):
        pass

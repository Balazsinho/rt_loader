# -*- coding: utf-8 -*-

import settings
from downloader.fileloader import FileLoader
from processors.mailparser import MailParser
from dataloader.nyilvantarto import Nyilvantarto  # @UnusedImport
from dataloader.leszereles import Leszereles  # @UnusedImport
from dataloader.new_db import NewDb  # @UnusedImport

from munka import MunkaLoader

from settings import LOADERS


class FileUpload(MunkaLoader):

    """
    Uploads and deletes the files stored in settings.MAIL_UPLOAD_DIR
    """

    def pre_run(self, args):
        self.email_acc = settings.MAIL_UPLOAD_DIR
        self.downloader = FileLoader(self.logger)
        self.parser = MailParser(self.logger)
        self.dataloaders = [globals()[loader_cls](self.logger)
                            for loader_cls in LOADERS['fileupload']]

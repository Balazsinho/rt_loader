# -*- coding: utf-8 -*-

import settings
from downloader.fileloader import FileLoader
from processors.mailparser import MailParser
from dataloader.leszereles import Leszereles
from dataloader.new_db import NewDb

from munka import MunkaLoader


class FileUpload(MunkaLoader):

    """
    Uploads and deletes the files stored in settings.MAIL_UPLOAD_DIR
    """

    def pre_run(self, args):
        self.email_acc = settings.MAIL_UPLOAD_DIR
        self.downloader = FileLoader(self.logger)
        self.parser = MailParser(self.logger)
        self.dataloaders = (
            # Nyilvantarto(self.logger, settings.GYURI_DB),
            # Leszereles(self.logger, settings.GYURI_DB),
            # NewDb(self.logger),
        )

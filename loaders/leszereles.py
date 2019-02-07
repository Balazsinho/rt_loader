# -*- coding: utf-8 -*-

import settings
from downloader.downloader import Downloader
from processors.mailparser import MailParser

from email_base import EmailLoaderBase

from settings import LOADERS


class LeszerelesLoader(EmailLoaderBase):

    """
    Processes the emails in the ACC_LESZERELES email account.
    After the emails are processed, we need to remove the successful ones
    from the inbox folder.
    """

    def pre_run(self):
        super(LeszerelesLoader, self).pre_run()
        self.email_acc = settings.ACC_LESZERELES_OLD
        self.downloader = Downloader(self.logger)
        self.parser = MailParser(self.logger)
        self.dataloaders = []
        for loader_cls_name in LOADERS['leszereles']:
            loader_module = __import__('dataloader')
            cls = getattr(loader_module, loader_cls_name)
            self.dataloaders.append(cls(self.logger))

# -*- coding: utf-8 -*-

import settings
from downloader.downloader import Downloader
from processors.mailparser import MailParser

from email_base import EmailLoaderBase

from settings import LOADERS


class InfoLoader(EmailLoaderBase):

    def pre_run(self, args):
        super(InfoLoader, self).pre_run(args)
        self.email_acc = settings.ACC_INFO
        self.downloader = Downloader(self.logger)
        self.parser = MailParser(self.logger)
        self.dataloaders = []
        for loader_cls_name in LOADERS['info']:
            loader_module = __import__('dataloader')
            cls = getattr(loader_module, loader_cls_name)
            self.dataloaders.append(cls(self.logger))

    def _filter(self, mail):
        if mail.mail_from not in ('wfms_eventus@telekom.hu'):
            self.logger.debug(u'Levél átugrása innen: {}'
                              u''.format(mail.mail_from))
            return True
        return False

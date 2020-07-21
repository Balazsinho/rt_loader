# -*- coding: utf-8 -*-

import settings
from downloader.downloader import Downloader
from processors.mailparser import MailParser

from email_base import EmailLoaderBase

from settings import LOADERS


class InfoLoader(EmailLoaderBase):

    def pre_run(self):
        super(InfoLoader, self).pre_run()
        self.email_acc = settings.ACC_INFO
        self.downloader = Downloader(self.logger)
        self.parser = MailParser(self.logger)
        self.dataloaders = []
        for loader_cls_name in LOADERS['info']:
            loader_module = __import__('dataloader')
            cls = getattr(loader_module, loader_cls_name)
            self.dataloaders.append(cls(self.logger))

    def _filter(self, mail):
        from_wfms = 'wfms_eventus@telekom.hu' in mail.mail_from
        wfms_ticket = 'WFMS_Munkaelrendel' in mail.mail_subject
        if not from_wfms and not wfms_ticket:
            self.logger.debug('Mail skipped from: {}'
                              ''.format(mail.mail_from))
            return True
        return False

    def _post_process(self, new_mails):
        pass

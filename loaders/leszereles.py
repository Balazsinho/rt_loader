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

    def __init__(self, *args, **kwargs):
        EmailLoaderBase.__init__(self, *args, **kwargs)
        self._marked_to_del_idxs = []

    def pre_run(self):
        super(LeszerelesLoader, self).pre_run()
        self.email_acc = settings.ACC_LESZERELES
        self.downloader = Downloader(self.logger)
        self.parser = MailParser(self.logger)
        self.dataloaders = []
        for loader_cls_name in LOADERS['leszereles']:
            loader_module = __import__('dataloader')
            cls = getattr(loader_module, loader_cls_name)
            self.dataloaders.append(cls(self.logger))

    def _duplicate(self, mail):
        EmailLoaderBase._duplicate(self, mail)
        self._marked_to_del_idxs.append(mail.idx)

    def _notproc(self, mail):
        self._duplicates += 1

    def _error(self, mail):
        self._duplicates += 1

    def _success(self, mail):
        super(LeszerelesLoader, self)._success(mail)
        self._marked_to_del_idxs.append(mail.idx)

    def _post_process(self, *args):
        self.downloader.delete_mails(self.email_acc, self._marked_to_del_idxs)

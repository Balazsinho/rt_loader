# -*- coding: utf-8 -*-

import settings
from downloader.downloader import Downloader
from processors.mailparser import MailParser

from email_base import EmailLoaderBase

from settings import LOADERS


class MunkaLoader(EmailLoaderBase):

    """
    Processes the emails in the ACC_MUNKA email account. After the emails are
    processed, we need to remove the successful ones from the inbox folder.
    """

    def pre_run(self):
        super(MunkaLoader, self).pre_run()
        self.email_acc = settings.ACC_MUNKA
        self.downloader = Downloader(self.logger)
        self.parser = MailParser(self.logger)
        self.dataloaders = []
        for loader_cls_name in LOADERS['munka']:
            loader_module = __import__('dataloader')
            cls = getattr(loader_module, loader_cls_name)
            self.dataloaders.append(cls(self.logger))

    def _post_process(self, new_mails):
        marked_for_delete_idxs = [mail.idx for mail in new_mails
                                  if mail.status == mail.OK]
        self.logger.info(u'Törlendő emailek: {}'
                         u''.format(str(marked_for_delete_idxs)))

        if not self._args.dry_run and not self._args.raw:
            self.downloader.delete_mails(self.email_acc,
                                         marked_for_delete_idxs)
            self.logger.info(u'Törlés kész')
        else:
            self.logger.info(u'Teszt mód, nincs törlés')

# -*- coding: utf-8 -*-

import os

import settings
from file_upload import FileUpload
from downloader.fileloader import FileLoader


class ErrorRetry(FileUpload):

    """
    Uploads and deletes the files stored in settings.MAIL_ERROR_DIR
    """

    def pre_run(self):
        super(ErrorRetry, self).pre_run()
        self.downloader = FileLoader(self.logger)
        self.email_acc = settings.EMAIL_ERROR_DIR

    def _error(self, mail):
        pass

    def _success(self, mail):
        super(ErrorRetry, self)._success(mail)
        filename = os.path.join(self.email_acc, mail.filename)
        os.remove(filename)

    def _duplicate(self, mail):
        # super(ErrorRetry, self)._success(mail)
        filename = os.path.join(self.email_acc, mail.filename)
        os.remove(filename)

    def _post_process(self, new_mails):
        pass

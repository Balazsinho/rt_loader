# -*- coding: utf-8 -*-

import settings
from file_upload import FileUpload


class ErrorRetry(FileUpload):

    """
    Uploads and deletes the files stored in settings.MAIL_ERROR_DIR
    """

    def pre_run(self, args):
        super(ErrorRetry, self).pre_run(args)
        self.email_acc = settings.EMAIL_ERROR_DIR

    def _duplicate(self):
        pass

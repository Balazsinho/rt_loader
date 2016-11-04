# -*- coding: utf-8 -*-

import os
import codecs
import traceback

import settings
from downloader.mail import Mail
from dataloader.base import DuplicateItemError
from loaders.base import (LoaderBase, NotProcessableEmailError,
                          LoaderException, ErrorsDuringProcess)


class EmailLoaderBase(LoaderBase):

    STATUS_DIR_MAP = {
        Mail.OK: settings.EMAIL_SUCCESS_DIR,
        Mail.ERROR: settings.EMAIL_ERROR_DIR,
        Mail.NOTPROC: settings.EMAIL_NOTPROC_DIR,
    }

    def __init__(self, *args, **kwargs):
        super(EmailLoaderBase, self).__init__(*args, **kwargs)

    def _filter(self, mail):
        pass

    def _extract(self, mail):
        self.logger.info(u'--- Feldolgozás alatt: {}'
                         u''.format(mail.filename))

        if not mail.html:
            raise NotProcessableEmailError(u'Nem feldolgozható email: '
                                           u'{}'.format(mail.filename))
        if not self._args.raw:
            extracted_data = self.parser.parse(mail.html)
        else:
            extracted_data = self.parser.extract_raw(mail.html)

        return extracted_data

    def run(self):
        # Download the mails
        try:
            new_mails = self.downloader.fetch_mails(self.email_acc)
        except Exception as e:
            raise LoaderException(u'Email lekérdezés sikertelen: {}'.format(e))

        error_count = 0
        for mail in new_mails:
            try:
                if self._filter(mail):
                    continue

                self._filter_attachments(mail)
                extracted_data = self._extract(mail)

            except NotProcessableEmailError as e:
                self.logger.warning(u'{}: {}'.format(mail.filename, e))
                mail.status = mail.NOTPROC

            except Exception as e:
                # =============================================================
                # Something went wrong, log the error and mark the email as
                # errorneous
                # =============================================================
                error_count += 1
                self.logger.error(u'{}: {}'.format(mail.filename, e))
                mail.status = mail.ERROR
                traceback.print_exc()

            else:
                if not self._args.dry_run and not self._args.raw:
                    for l in self.dataloaders:
                        try:
                            self.logger.info(u'Feltöltő futtatása: {}'
                                             u''.format(l.__class__.__name__))
                            l.insert_mail_data(extracted_data, mail)

                        except DuplicateItemError as e:
                            self.logger.debug(u'{}: {}'.format(mail.filename, e))
                            mail.status = mail.DUPLICATE
                            self._duplicate()

                        except Exception as e:
                            # =================================================
                            # Something went wrong, log the error and mark the
                            # email as errorneous
                            # =================================================
                            error_count += 1
                            self.logger.error(u'{}: {}'.format(mail.filename, e))
                            mail.status = mail.ERROR
                            traceback.print_exc()

            if self._args.raw:
                self.logger.info(u'*** Következő rekord')
                continue

            self.logger.info(u'Feldolgozás {}'.format(
                u'OK' if mail.status == mail.OK else u'HIBA'))
            # =================================================================
            # Write the email into the appropriate directory
            # =================================================================
            if not self._args.dry_run:
                if mail.status == mail.OK:
                    self._success(mail)
                elif mail.status == mail.ERROR:
                    self._error(mail)
                elif mail.status == mail.NOTPROC:
                    self._notproc(mail)

        self.logger.info(u'--- Email feldolgozás kész {} hibaval ---'
                         u''.format(error_count))

        self._post_process(new_mails)

        if error_count > 0:
            raise ErrorsDuringProcess()

    def _filter_attachments(self, mail):
        """
        Fork for filtering useful attachments
        """
        mail.attachments = dict([(k, v) for k, v
                                 in mail.attachments.iteritems()
                                 if 'imdb' in k.lower()])

    def _success(self, mail):
        """
        Fork for handling successful emails
        """
        super(EmailLoaderBase, self)._success(mail)
        self._write(mail)

    def _error(self, mail):
        """
        Fork for handling errors during email processing
        """
        super(EmailLoaderBase, self)._error(mail)
        self._write(mail)

    def _notproc(self, mail):
        """
        Fork for handling not processable emails
        """
        super(EmailLoaderBase, self)._notproc(mail)
        self._write(mail)

    def _write(self, mail):
        """
        Writes an email to the appropriate directory
        """
        path = self.STATUS_DIR_MAP[mail.status]
        filename = os.path.join(path, mail.filename)
        with codecs.open(filename, 'w') as mail_file:
            mail_file.write(mail.html)  # or u'<br />\n'.join(map(unidecode, mail.raw)))
            self.logger.info(u'File kiírva: {}'.format(mail_file.name))

# -*- coding: utf-8 -*-

import os
import codecs

import settings
from downloader.downloader import Downloader
from processors.mailparser import MailParser

from dataloader.base import DuplicateItemError
from dataloader.nyilvantarto import Nyilvantarto
from dataloader.leszereles import Leszereles
from dataloader.new_db import NewDb
from utils.pprinter import PPrinter

from base import LoaderBase
from loaders.base import LoaderException
from loaders.base import NotProcessableEmailError

from settings import LOADERS


class InfoLoader(LoaderBase):

    def pre_run(self, args):
        self.email_acc = settings.ACC_INFO
        self.downloader = Downloader(self.logger)
        self.parser = MailParser(self.logger)
        self.dataloaders = [globals()[loader_cls](self.logger)
                            for loader_cls in LOADERS['info']]

    def run(self, args):
        # Download the mails
        try:
            new_mails = self.downloader.fetch_mails(self.email_acc)
        except Exception as e:
            raise LoaderException(u'Email lekérdezés sikertelen: {}'.format(e))

        # Create the mail download directories
        if not os.path.exists(settings.EMAIL_SUCCESS_DIR):
            os.makedirs(settings.EMAIL_SUCCESS_DIR)

        if not os.path.exists(settings.EMAIL_ERROR_DIR):
            os.makedirs(settings.EMAIL_ERROR_DIR)

        if not os.path.exists(settings.EMAIL_NOTPROC_DIR):
            os.makedirs(settings.EMAIL_NOTPROC_DIR)

        error_count = 0
        for mail in new_mails:
            email_dir = settings.EMAIL_SUCCESS_DIR
            try:
                if mail.mail_from not in ('wfms_eventus@telekom.hu'):
                    self.logger.debug(u'Level atugrasa innen: {}'
                                      u''.format(mail.mail_from))
                    continue

                if not mail.html:
                    raise NotProcessableEmailError(u'Nem feldolgozható email: {}'
                                                   u''.format(mail.filename))

                # =================================================================
                # Try to extract and load the data
                # =================================================================
                self.logger.info(u'--- Feldolgozás alatt: {}'
                                 u''.format(mail.filename))

                if not args.raw:
                    extracted_data = self.parser.parse(mail.html)
                else:
                    extracted_data = self.parser.extract_raw(mail.html)

                PPrinter().pprint(extracted_data)

            except NotProcessableEmailError as e:
                self.logger.warning(u'{}: {}'.format(mail.filename, e))
                email_dir = settings.EMAIL_NOTPROC_DIR

            except Exception as e:
                # =================================================================
                # Something went wrong, log the error and mark the email as
                # errorneous
                # =================================================================
                error_count += 1
                email_dir = settings.EMAIL_ERROR_DIR
                self.logger.error(u'{}: {}'.format(mail.filename, e))

            else:
                if not args.dry_run and not args.raw:
                    for l in self.dataloaders:
                        try:
                            self.logger.info(u'Feltolto futtatasa: {}'
                                             u''.format(l.__class__.__name__))
                            l.insert_mail_data(extracted_data, mail.html)

                        except DuplicateItemError as e:
                            self.logger.info(u'{}: {}'.format(mail.filename, e))
                            self._duplicate()

                        except Exception as e:
                            # =================================================================
                            # Something went wrong, log the error and mark the email as
                            # errorneous
                            # =================================================================
                            error_count += 1
                            email_dir = settings.EMAIL_ERROR_DIR
                            self.logger.error(u'{}: {}'.format(mail.filename, e))

            if args.raw:
                self.logger.info('*** Kovetkezo rekord')
                continue

            self.logger.info(u'Feldolgozás {}'.format(
                'OK' if email_dir == settings.EMAIL_SUCCESS_DIR else 'HIBA'))
            # =================================================================
            # Write the email into the appropriate directory
            # =================================================================
            if not args.dry_run:
                mail_output_filename = os.path.join(email_dir, mail.filename)
                with codecs.open(mail_output_filename, 'w') as mail_file:
                    mail_file.write(mail.html)
                    self.logger.info(u'File kiírva: {}'.format(mail_file.name))

        self.logger.info(u'--- Email feldolgozás kész {} hibaval ---'
                         ''.format(error_count))

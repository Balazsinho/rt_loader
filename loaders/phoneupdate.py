# -*- coding: utf-8 -*-

import os
import xlrd

import settings
from dataloader.leszereles import Leszereles

from base import LoaderBase
from loaders.base import LoaderException
from utils import create_and_list_dir


class PhoneUpdateLoader(LoaderBase):

    def run(self):
        files_to_process = create_and_list_dir(self.logger,
                                               settings.PHONEUPD_DIR)
        leszereles = Leszereles(self.logger)

        for f in files_to_process:
            workbook = xlrd.open_workbook(f)
            worksheet = workbook.sheet_by_index(0)
            for row in xrange(worksheet.nrows):
                try:
                    mt_id = str(int(worksheet.cell_value(row, 0)))
                except Exception as e:
                    self.logger.warning(u'Érvénytelen MT ID formátum: {}'
                                        u''.format(worksheet.cell_value(row,
                                                                        0)))
                    continue

                numbers = []
                for col in xrange(1, worksheet.ncols):
                    phone_num = worksheet.cell_value(row, col)
                    if not phone_num:
                        break
                    numbers.append(phone_num)

                numbers_str = ', '.join(numbers)
                self.logger.debug(u'Adatok írása: {} - {}'
                                  u''.format(mt_id, numbers_str))

                if numbers_str.strip():
                    try:
                        leszereles.update_phone_number(mt_id, numbers_str)
                    except Exception as e:
                        raise LoaderException(e)

                if row > 0 and row % 100 == 0:
                    self.logger.info(u'{} sor beírva'.format(row))

            done_file = os.path.join(settings.PHONEUPD_SUCCESS_DIR,
                                     os.path.split(f)[1])
            self.logger.info(u'Kész file írása: {}'
                             u''.format(done_file))
            os.rename(f, done_file)

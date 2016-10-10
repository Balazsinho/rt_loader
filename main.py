# -*- coding: utf-8 -*-

import logging
from logging.config import dictConfig
import argparse

import settings
from loaders.base import StopException
from loaders.munka import MunkaLoader
from loaders.info import InfoLoader
from loaders.phoneupdate import PhoneUpdateLoader
from loaders.file_upload import FileUpload


LOADERS = (
    PhoneUpdateLoader,
    InfoLoader,
    MunkaLoader,
    FileUpload,
)


if __name__ == '__main__':
    # =========================================================================
    # LOGGER
    # =========================================================================
    logger = logging.getLogger()
    dictConfig(settings.LOGGING_CONF)

    # =========================================================================
    # ARGS
    # =========================================================================
    parser = argparse.ArgumentParser(description='Rövid-táv email processing')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true',
                        help='Do not perform any insertions/deletions/writes')
    parser.add_argument('--raw', dest='raw', action='store_true',
                        help='Show the unfiltered extraction result (raw)')

    args = parser.parse_args()

    if args.dry_run:
        logger.info(u'* DRY RUN - Csak feldolgozás teszt, nem történik írás')
    if args.raw:
        logger.info(u'* RAW - a nyers kinyert adatokat listázza, '
                    u'szűrés nélkül')

    for loader in LOADERS:
        loader_inst = loader(logger)
        logger.info(u'Betöltő futtatása: {}'
                    u''.format(loader_inst.__class__.__name__))
        try:
            loader_inst.pre_run(args)
            loader_inst.run(args)
        except StopException as e:
            logger.error(u'Feldolgozás vége: {}'.format(e))
        except Exception as e:
            logger.error(u'Hiba a feldolgozás közben: {}'.format(e))
        finally:
            logger.info(u'Kész')

    logger.info(u'-- Összes kész')

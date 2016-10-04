# -*- coding: utf-8 -*-

import sys
import logging
from logging.config import dictConfig
from processors import reports
import settings


if __name__ == '__main__':
    # =========================================================================
    # LOGGER
    # =========================================================================
    logger = logging.getLogger()
    dictConfig(settings.REPORT_LOGGING_CONF)

    avail_reports = reports.available_reports()
    avail_report_keys = avail_reports.keys()
    print '*** Riport valasztas ***'
    while True:
        for idx, report_name in enumerate(avail_reports.keys()):
            print u'\t{} - {}'.format(idx+1, report_name)

        print u'\tQ - Kilepes'
        choice = raw_input('Melyiket futtassam? ')
        if choice == 'Q':
            print u'Kilepes'
            sys.exit(0)
        try:
            report_key = avail_report_keys[int(choice)-1]
            report_cls = avail_reports[report_key]
            print u'\n*** {} ***\n'.format(report_key)
            break
        except Exception as e:
            print u'Ervenytelen valasztas\n'
            continue

    report = report_cls(logger)
    report.initialize()
    report.execute()

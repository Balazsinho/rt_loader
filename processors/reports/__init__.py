# -*- coding: utf-8 -*-

from leszereles_elszamolas.report import LeszerelesElsz


def available_reports():
    return {
        'Leszereles elszamolas': LeszerelesElsz,
    }

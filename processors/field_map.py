# -*- coding: utf-8 -*-

import fieldprocessors
from field_const import Fields


# ==========================================================================
# KINYERT MEZŐK
# ==========================================================================
# ==========================================================================
# This is the field mapping from the document to the internal keys. An
# example:
#
# "MT ugyfel-azonosito" and "MT ID" are both mapped to MT_ID constant,
# so after the processing they can easily be accessed using that single
# identifier.
# ==========================================================================
USABLE_FIELDS = [

    # ======================================================================
    # MUNKALAP - RÉGI FORMÁTUM
    # ======================================================================
    # ('Adószám', Fields.),
    ('Az elofizetoi vegberendezes felszerelesenek a helye',
     Fields.ADDR1, [fieldprocessors.address]),
    ('EFP Megrendelesszam', Fields.EFP_NUM),
    ('KI Igenyazonosito', Fields.KI_ID),
    ('MT ugyfel-azonosito', Fields.MT_ID),
    ('Igenytipus', Fields.REQ_TYPE),
    ('Ertesitesi telefon', Fields.PHONE1),
    ('Nev (csaladi és utonev)', Fields.NAME1),
    ('WFMS jegyazonosito-Task Nr', Fields.TICKET_ID),
    ('WFMS jegy letrejotte', Fields.DATE_CREATED),
    ('Egyeztetett idopont', Fields.AGREED_TIME),
    ('Feladat tipus', Fields.TASK_TYPE, ),
    # [fieldprocessors.task_type]),

    # ======================================================================
    # HIBALAP - ÚJ FORMÁTUM
    # ======================================================================
    ('A szam', Fields.A_NUM),
    ('Bejelentes tipusa', Fields.REQ_TYPE),
    ('Hibaelharitasi hatarido [ora]', Fields.SLA_H),
    ('Hibajegy azonosito', Fields.TICKET_ID),
    ('Ugyfel neve', Fields.NAME1),
    ('Kapcsolattarto nev', Fields.NAME2),
    ('Kapcsolattarto telefon', Fields.PHONE1),
    ('MT ID', Fields.MT_ID),
    ('TASK ID', Fields.TASK_ID),
    ('Telepitesi cim', Fields.ADDR1,
     [fieldprocessors.address]),
    ('MT-azonosito', Fields.MT_ID),

    # ======================================================================
    # MUNKALAP - ÚJ FORMÁTUM
    # ======================================================================
    ('Egyeztetett idopont', Fields.AGREED_TIME),
    ('Elofizeto neve', Fields.NAME1),
    ('Igeny rogzites datuma', Fields.DATE_CREATED),
    ('Igeny tipus', Fields.REQ_TYPE),
    ('Jegyazonosito-Task Nr', Fields.TICKET_ID),
    ('Kapcsolattarto neve', Fields.NAME1),
    ('MT ugyfelazonosito', Fields.MT_ID),
    ('Megrendelesszam', Fields.ORDER_NUM),
    ('OSS ugyfelszam', Fields.OSS_ID),
    ('Telefonszam', Fields.PHONE2),
    ('Veteli hely', Fields.ADDR1,
     [fieldprocessors.address]),
    ('Letesitesi cime', Fields.ADDR1,
     [fieldprocessors.address]),
    # ('Értesítési telefon (Egyéb)', Fields.),
    # ('Értesítési telefon (Otthoni)', Fields.),

    # ======================================================================
    # MINDENFELE
    # ======================================================================
    ('Jegy azonosito', Fields.TICKET_ID),
    ('Felszerelesi cim', Fields.ADDR1),
    ('Ertesitesi szam', Fields.PHONE1),
    ('Feladat', Fields.TASK_TYPE,),
    # [fieldprocessors.task_type]),
    ('Kapcsolasi szam', Fields.MT_ID),
    ('Feladat megjegyzes', Fields.REMARKS),

    ('Kapcsolattarto', Fields.PHONE1),
    ('MT_ID', Fields.MT_ID),
    ('Nev (csaladi es utonev)', Fields.NAME1),
]


# To ensure that the calculated fields get the highest prority
# we append a (Fields.<field>, Fields.<field>) mapping to the
# end of the USABLE_FIELDS. This way it'll overwrite whatever is mapped
# to the field. During calculation we write the value directly to the
# Fields.<field> variable
# See fieldprocessors.py POSTPARSERS section for code

_field_v = vars(Fields)
for f in [v for v in _field_v if not v.startswith('_')]:
    USABLE_FIELDS.append((_field_v[f], _field_v[f]))


NAME_MAP = dict([(f[0].decode('utf-8'), f[1]) for f in USABLE_FIELDS])
PROCESSOR_MAP = dict([(f[1], f[2]) for f in USABLE_FIELDS if len(f) == 3])


def is_field_usable(field_name):
    return u'{}'.format(field_name) in NAME_MAP


def mapped_field(field_name):
    return NAME_MAP[field_name]


def processors(field_name):
    return PROCESSOR_MAP.get(field_name, [])

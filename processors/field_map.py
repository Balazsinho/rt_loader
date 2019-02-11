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

    ('Hibajegy azonosito', Fields.TICKET_ID),
    ('WFMS jegyazonosito-Task Nr', Fields.TICKET_ID),
    ('Jegyazonosito-Task Nr', Fields.TICKET_ID),
    ('Jegy azonosito', Fields.TICKET_ID),

    ('A szam', Fields.A_NUM),
    ('OSS ugyfelszam', Fields.OSS_ID),
    ('KI Igenyazonosito', Fields.KI_ID),
    ('TASK ID', Fields.TASK_ID),
    ('EFP Megrendelesszam', Fields.EFP_NUM),
    ('Megrendelesszam', Fields.ORDER_NUM),

    ('WFMS jegy letrejotte', Fields.DATE_CREATED),
    ('Beerkezes datuma', Fields.DATE_CREATED),
    ('Igeny rogzites datuma', Fields.DATE_CREATED),
    ('Egyeztetett idopont', Fields.AGREED_TIME_RAW),

    ('Bejelentes tipusa', Fields.REQ_TYPE),
    ('Igeny tipus', Fields.REQ_TYPE),
    ('Igenytipus', Fields.REQ_TYPE),

    ('Feladat tipus', Fields.TASK_TYPE),
    ('Feladat', Fields.TASK_TYPE,),

    ('Hibaelharitasi hatarido [ora]', Fields.SLA_H),
    # ('Feladat megjegyzes', Fields.REMARKS),
    # ('Leiras', Fields.REMARKS),

    ('Veteli hely', Fields.ADDR1,
     [fieldprocessors.address]),
    ('Letesitesi cime', Fields.ADDR1,
     [fieldprocessors.address]),
    ('Felszerelesi cim', Fields.ADDR1,
     [fieldprocessors.address]),
    ('Telepitesi cim', Fields.ADDR1,
     [fieldprocessors.address]),
    ('Az elofizetoi vegberendezes felszerelesenek a helye',
     Fields.ADDR1, [fieldprocessors.address]),

    ('Nev (csaladi es utonev)', Fields.NAME1),
    ('Kapcsolattarto neve', Fields.NAME1),
    ('Ugyfel neve', Fields.NAME1),
    ('Elofizeto neve', Fields.NAME1),
    ('Nev (csaladi és utonev)', Fields.NAME1),
    ('Kapcsolattarto nev', Fields.NAME2),

    ('Ertesitesi szam', Fields.PHONE1),
    ('Kapcsolattarto', Fields.PHONE1),
    ('Kapcsolattarto telefon', Fields.PHONE1),
    ('Ertesitesi telefon', Fields.PHONE1),
    ('Ertesitesi telefon (Otthoni)', Fields.PHONE2),
    ('Telefonszam', Fields.PHONE2),

    ('MT ugyfel-azonosito', Fields.MT_ID),
    ('MT ugyfelazonosito', Fields.MT_ID),
    ('Kapcsolasi szam', Fields.MT_ID),
    ('MT ID', Fields.MT_ID),
    ('MT_ID', Fields.MT_ID),
    ('MT-azonosito', Fields.MT_ID),
]


# To ensure that the calculated fields get the highest prority
# we append a (Fields.<field>, Fields.<field>) mapping to the
# end of the USABLE_FIELDS. This way it'll overwrite whatever is mapped
# to the field. During calculation we write the value directly to the
# Fields.<field> variable
# See fieldprocessors.py POSTPARSERS section for code

_field_v = vars(Fields)
final_field_names = [v for v in _field_v if not v.startswith('_')]
FINAL_FIELDS = [_field_v[f] for f in final_field_names]
USABLE_FIELDS.extend([(f, f) for f in FINAL_FIELDS])

NAME_MAP = dict([(f[0].decode('utf-8'), f[1]) for f in USABLE_FIELDS])
PROCESSOR_MAP = dict([(f[1], f[2]) for f in USABLE_FIELDS if len(f) == 3])


def is_field_usable(field_name):
    return u'{}'.format(field_name) in NAME_MAP


def mapped_field(field_name):
    return NAME_MAP[field_name]


def processors(field_name):
    return PROCESSOR_MAP.get(field_name, [])

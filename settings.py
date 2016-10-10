import logging
import os

DEBUG = False

PROJECT_DIR = os.path.dirname(__file__)

EMAIL_SUCCESS_DIR = os.path.join(PROJECT_DIR, 'files', 'success')
EMAIL_ERROR_DIR = os.path.join(PROJECT_DIR, 'files', 'error')
EMAIL_NOTPROC_DIR = os.path.join(PROJECT_DIR, 'files', 'not_proc')

PHONEUPD_DIR = os.path.join(PROJECT_DIR, 'files', 'phone_update')
PHONEUPD_SUCCESS_DIR = os.path.join(PROJECT_DIR, 'files', 'phone_update',
                                    'done')

MAIL_UPLOAD_DIR = os.path.join(PROJECT_DIR, 'files', 'mail_upload')

REPORT_OUTPUT_DIR = os.path.join(PROJECT_DIR, 'reports')

GYURI_DB = {
    'server': 'SZERVER',
    'port': '8778',
    'user': 'Szerver\\SysRoot',
    'pass': '100kurva',
}

ROVIDTAV_SERVER = '213.181.208.4'
ROVIDTAV_AUTH = 'mailUploader:Upl04D'

ACC_MUNKA = 'munka'
ACC_INFO = 'info'

EMAIL_ACCS = {
    ACC_MUNKA: {
        'host': 'mail.rovid-tav.hu',
        'port': 110,
        'user': 'munka@rovid-tav.hu',
        'passwd': 'hu7EyieW',
    },
    ACC_INFO: {
        'host': 'mail.rovid-tav.hu',
        'port': 110,
        'user': 'info@rovid-tav.hu',
        'passwd': 'eiTa6wah',
    }
}

# =============================================================================
# Loader configuration
# =============================================================================

# Classes
LESZERELES = 'Leszereles'
NYILVANTARTO = 'Nyilvantarto'
NEWDB = 'NewDb'

# Config
LOADERS = {
    'info': (NEWDB, NYILVANTARTO, LESZERELES),
    'munka': (NEWDB, NYILVANTARTO, LESZERELES),
    'fileupload': (NEWDB, NYILVANTARTO, LESZERELES),
}

# =============================================================================
# Logging configuration
# =============================================================================

LOGLEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGING_CONF = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': LOGLEVEL,
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'level': LOGLEVEL,
            # 'encoding': 'utf-8',
            'filename': os.path.join(PROJECT_DIR, 'process.log'),
        },
    },
    'root': {
        'handlers': ['stream', 'file'],
        'level': LOGLEVEL,
    },
}

REPORT_LOGGING_CONF = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': LOGLEVEL,
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'level': LOGLEVEL,
            # 'encoding': 'utf-8',
            'filename': os.path.join(PROJECT_DIR, 'reports.log'),
        },
    },
    'root': {
        'handlers': ['stream', 'file'],
        'level': LOGLEVEL,
    },
}

try:
    from local_settings import *
except ImportError:
    pass

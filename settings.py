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

SCAN_DIR = os.path.join(PROJECT_DIR, 'files', 'scans')

# =============================================================================
# Loader configuration
# =============================================================================

# Classes
LESZERELES = 'Leszereles'
NYILVANTARTO = 'Nyilvantarto'
NEWDB = 'NewDb'
NEWDBUNINST = 'NewDbUninst'

# Config
LOADERS = {
    'info': (NEWDB,),
    'leszereles': (NEWDBUNINST,),
    'munka': (NEWDB,),
    'fileupload': (NEWDBUNINST,),
    'scan': (NEWDB,),
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

import os
from app.logs import RequestFilter


class Config():
    """Default dev configuration"""

    # Directories
    APP_DIR = os.path.dirname(__file__)
    STATIC_DIR = os.path.join(APP_DIR, 'static')

    # Logging
    LOGCONFIG = {
        'version': 1,
        'formatters': {
            'default': {
                'format': ('[%(ip)s %(requestID)s] [%(method)s %(path)s] '
                           '[%(asctime)s] [%(name)s %(levelname)s] '
                           '[%(status)s] %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S %Z%z'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'filters': ['RequestFilter']
            },
            'rotfile': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/main.log',
                'maxBytes': 10485760,  # 10 Mb
                'backupCount': 10,
                'formatter': 'default',
                'filters': ['RequestFilter'],
            }
        },
        'filters': {
            'RequestFilter': {
                '()': RequestFilter
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'rotfile']
        }
    }


class TestConfig(Config):
    TESTING = True

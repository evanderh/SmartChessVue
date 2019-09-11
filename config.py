import os
from BenderChess.logs import RequestFilter


class Config():
    """Default dev configuration"""

    # General
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-dev-key'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Directories
    APP_DIR = os.path.dirname(__file__)
    DIST_DIR = os.path.join(APP_DIR, 'dist')

    # Logging
    LOGCONFIG = {
        'version': 1,
        'formatters': {
            'default': {
                'format': ('[%(ip)s] [%(method)s %(path)s] [%(asctime)s] '
                           '[%(name)s %(levelname)s] %(message)s'),
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
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URL')
    TEST_USER = 'testuser'
    TEST_PASS = 'testpass'

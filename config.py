import os


class Config():
    """Default dev configuration"""

    # General
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-dev-key'
    SERVER_NAME = "bender.localhost:5000"

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URL')
    TEST_USER = 'testuser'
    TEST_PASS = 'testpass'

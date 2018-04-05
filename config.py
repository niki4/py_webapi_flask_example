class Config(object):
    DEBUG = False
    TESTING = False
    DB_URI = 'sqlite://:memory:'
    BASE_URL = '/api/v1/'
    PORT = 5000


class ProductionConfig(Config):
    DB_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DB_URI = 'sqlite:///db.sqlite'
    HOST = 'localhost'

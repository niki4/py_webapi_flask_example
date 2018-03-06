class Config(object):
    DEBUG = False
    TESTING = False
    DB_URI = 'sqlite://:memory:'


class ProductionConfig(Config):
    DB_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

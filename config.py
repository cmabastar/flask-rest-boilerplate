class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TOKEN_EXPIRATION_TIME = 3600

    # Define the application directory
    import os
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Log file (the directory must exist)
    APPLICATION_LOG = os.path.join(BASE_DIR, 'log', 'application.log')
    ACCESS_LOG = os.path.join(BASE_DIR, 'log', 'access.log')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://test:test123@localhost/flask"
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


# Default configuration
default = DevelopmentConfig

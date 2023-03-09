from decouple import config, Csv

POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
POSTGRES_DB = config('POSTGRES_DB')
POSTGRES_HOST = config('POSTGRES_HOST', default='localhost')
POSTGRES_PORT = config('POSTGRES_PORT', cast=int, default=5432)

TEST_POSTGRES_USER = config('TEST_POSTGRES_USER')
TEST_POSTGRES_PASSWORD = config('TEST_POSTGRES_PASSWORD')
TEST_POSTGRES_DB = config('TEST_POSTGRES_DB')
TEST_POSTGRES_HOST = config('TEST_POSTGRES_HOST', default='localhost')
TEST_POSTGRES_PORT = config('TEST_POSTGRES_PORT', cast=int, default=5431)


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://' \
                              f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
                              f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://' \
                              f'{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}@' \
                              f'{TEST_POSTGRES_HOST}:{TEST_POSTGRES_PORT}/{TEST_POSTGRES_DB}'


class DebugConfig(BaseConfig):
    DEBUG = True

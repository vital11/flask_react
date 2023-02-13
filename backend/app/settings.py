from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')

POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
POSTGRES_DB = config('POSTGRES_DB')
POSTGRES_HOST = config('POSTGRES_HOST', default='localhost')
POSTGRES_PORT = config('POSTGRES_PORT', cast=int, default=5432)

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
                          f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

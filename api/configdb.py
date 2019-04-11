from os import environ


MYSQL = environ.get('DB_HOST', '127.0.0.1')
DATABASE = environ.get('DATABASE', 'todo')
PASS = environ.get('PASS', 'password')
USER = environ.get('USER', 'user') if environ.get(
    'MODE') == 'production' else 'user'

DB_URI = 'mysql://{}:{}@{}'.format(
    USER,
    PASS,
    MYSQL
)

SQLALCHEMY_DATABASE_URI = '{}/{}'.format(
    DB_URI,
    DATABASE
)

SQLALCHEMY_TRACK_MODIFICATIONS = True

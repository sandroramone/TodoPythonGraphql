from os import environ
from api import create_api
from sqlalchemy import create_engine

from models.database import create_db
from configdb import DATABASE, DB_URI


MODE = environ.get('MODE', 'development')
app = create_api(MODE)

engine = create_engine(DB_URI)
databases = engine.execute('SHOW DATABASES')
databases = [d[0] for d in databases]

if DATABASE not in databases:
    engine.execute("CREATE DATABASE IF NOT EXISTS {} ".format(DATABASE))
    create_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0')

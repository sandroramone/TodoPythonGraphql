from models.base import db
from models.todo import TodoModel


def create_db():
    from sqlalchemy import create_engine
    from configdb import SQLALCHEMY_DATABASE_URI
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    db.metadata.drop_all(engine)
    db.metadata.create_all(engine)

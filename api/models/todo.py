from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Column
)
from sqlalchemy.orm import relationship

from models.base import db


class TodoModel(db.Model):
    """ Todo model representation """
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    description = Column(String(200), nullable=False)
    parent = Column(Integer, ForeignKey('todo.id'), nullable=True)

    related_tasks = relationship('TodoModel')

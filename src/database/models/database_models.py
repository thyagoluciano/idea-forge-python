# src/database/models/database_models.py
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import MetaData

metadata = MetaData()


class Base(declarative_base(metadata=metadata)):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
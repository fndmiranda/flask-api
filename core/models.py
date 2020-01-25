import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

engine = create_engine('sqlite:///database.sqlite')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class ModelMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    _default_limit = 25
    _max_limit = 100

    id = Column(Integer, primary_key=True)

    @classmethod
    def get_default_limit(cls, options={}):
        """Get retrieve limit of registers."""
        limit = int(options.get('limit', cls._default_limit))
        return limit if limit <= cls._max_limit else cls._max_limit

    @classmethod
    def get_max_limit(cls):
        """Get max retrieve limit of registers."""
        return cls._max_limit


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

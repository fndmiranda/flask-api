from flask import current_app
from peewee import Model
from peewee import SqliteDatabase

database = SqliteDatabase('database.sqlite')


class BaseModel(Model):
    class Meta:
        database = database
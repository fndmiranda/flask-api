from peewee import Model, SqliteDatabase

database = SqliteDatabase('database.sqlite')


class BaseModel(Model):
    class Meta:
        database = database

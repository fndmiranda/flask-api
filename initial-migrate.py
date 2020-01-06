from playhouse.migrate import SqliteDatabase
from playhouse.migrate import SqliteMigrator
from user.models import User


# @Todo: This file will be used before implementing the migration feature.
db = SqliteDatabase('database.sqlite')
migrator = SqliteMigrator(db)


def create_tables():
    with db:
        db.create_tables([User])


create_tables()

from peewee import Model, SqliteDatabase

database = SqliteDatabase('database.sqlite')


class BaseModel(Model):
    """Class representing the abstract base model."""

    _limit = 25
    _max_limit = 100
    _resource = None

    class Meta:
        database = database

    @classmethod
    def get_limit(cls):
        """Get register limit."""
        return cls._limit

    @classmethod
    def get_max_limit(cls):
        """Get max register limit."""
        return cls._max_limit

    @classmethod
    def get_resource(cls):
        """Get fields resource."""
        return cls._resource

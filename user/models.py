from core.models import BaseModel
from peewee import CharField, DateTimeField
from user.resources import user as resource


class User(BaseModel):
    _resource = resource()

    name = CharField()
    email = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'users'

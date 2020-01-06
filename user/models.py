from core.models import BaseModel
from peewee import CharField, DateTimeField


class User(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'users'

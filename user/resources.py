from core import fields
from core.resources import BaseResource


class User(BaseResource):
    _fields = {
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'is_admin': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

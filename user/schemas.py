from flask import request
from marshmallow import (
    validate,
    validates,
    Schema,
    fields,
    ValidationError,
    pre_load
)
from user.models import User


class UserSchema(Schema):
    id = fields.Integer(required=False, dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(min=3, max=255)])
    email = fields.Email(required=True, validate=[validate.Length(min=5, max=255)])
    is_admin = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(required=False, dump_only=True)
    updated_at = fields.DateTime(required=False, dump_only=True)
    password = fields.String(
        required=True, validate=[validate.Length(min=6, max=36)], load_only=True
    )

    @pre_load
    def pre_load(self, data, **kwargs):
        if request.method in ['PUT']:
            self.fields.get('password').required = False
        return data

    @validates('email')
    def validate_unique_email(self, data):
        from user.services import UserService

        user_id = request.view_args.get('user_id', None)

        if user_id is None:
            criterion = (User.email == data,)
        else:
            criterion = (User.email == data, User.id != user_id,)

        query = UserService().filter(*criterion)

        if bool(query.count()):
            raise ValidationError('Email already exists.')


class MetaSchema(Schema):
    current_page = fields.Integer()
    per_page = fields.Integer()
    total = fields.Integer()


class LinkSchema(Schema):
    first = fields.Url()
    last = fields.Url()
    next = fields.Url()
    prev = fields.Url()


class UserQueryArgsSchema(Schema):
    page = fields.Integer()
    limit = fields.Integer()


class UserPaginationSchema(Schema):
    data = fields.List(fields.Nested(lambda: UserSchema()))
    links = fields.Nested(LinkSchema)
    meta = fields.Nested(MetaSchema)

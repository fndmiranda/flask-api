from marshmallow import Schema, fields


class MetaSchema(Schema):
    current_page = fields.Integer()
    per_page = fields.Integer()
    total = fields.Integer()


class LinkSchema(Schema):
    first = fields.Url()
    last = fields.Url()
    next = fields.Url()
    prev = fields.Url()


class QueryArgsSchema(Schema):
    page = fields.Integer()
    limit = fields.Integer()

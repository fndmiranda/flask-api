from flask_restful import fields


def user():
    return {
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

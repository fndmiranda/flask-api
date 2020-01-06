from flask import request
from flask_restful import Resource, marshal
from cerberus import Validator
from user.validations import user as validation
from user.resources import user as resource
from user.services import UserService


class UserList(Resource):
    def get(self):
        data = UserService().paginate()
        return data
        # query = UserService().get()
        # return [marshal(i, resource()) for i in query]

    def post(self):
        v = Validator(validation())

        if v.validate(request.json):
            data = UserService().create(request.json)

            return marshal(data, resource()), 201
        else:
            return v.errors, 400


class UserDetail(Resource):
    def get(self, user_id):
        data = UserService().get_or_404(user_id)
        return marshal(data, resource())

    def delete(self, user_id):
        UserService().delete_or_404(user_id)
        return {}, 204

    def put(self, user_id):
        v = Validator(validation())

        if v.validate(request.json):
            data = UserService().update_or_404(user_id, request.json)

            return marshal(data, resource())
        else:
            return v.errors, 400

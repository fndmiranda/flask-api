from flask import request
from flask_restful import Resource
from cerberus import Validator
from user.validations import user as validation
from user.resources import User as UserResource
from user.services import UserService


class UserList(Resource):
    def get(self):
        data = UserService().paginate()
        return UserResource().collection(data)

    def post(self):
        v = Validator(validation())

        if v.validate(request.json):
            data = UserService().create(request.json)

            return UserResource().make(data), 201
        else:
            return v.errors, 400


class UserDetail(Resource):
    def get(self, user_id):
        data = UserService().find_or_404(user_id)
        return UserResource().make(data)

    def delete(self, user_id):
        UserService().delete_or_404(user_id)
        return {}, 204

    def put(self, user_id):
        v = Validator(validation())

        if v.validate(request.json):
            data = UserService().update_or_404(user_id, request.json)

            return UserResource().make(data)
        else:
            return v.errors, 400

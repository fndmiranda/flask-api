import json
from flask import request, jsonify
from flask_restful import Resource
from playhouse.shortcuts import model_to_dict, dict_to_model
from cerberus import Validator
from user import validations
from user.models import User


class UserList(Resource):
    def get(self):
        return {'path': 'UserList_get'}

    def post(self):
        v = Validator(validations.user())

        if v.validate(request.json):
            inserted_id = User().insert(request.json).execute()
            response = model_to_dict(User().select().where(User.id == inserted_id).get())

            return jsonify(response)
        else:
            return v.errors, 400


class UserDetail(Resource):
    def get(self, user_id):
        return {'path': 'UserDetail_get', 'user_id': user_id}

    def delete(self, user_id):
        return {'path': 'UserDetail_get', 'user_id': user_id}, 204

    def put(self, user_id):
        v = Validator(validations.user())

        if v.validate(request.json):
            # response = service.update({'_id': user_id}, request.json)
            # del response['password']
            response = request.json  # Todo: Insert logical here

            return jsonify(response)
        else:
            return v.errors, 400

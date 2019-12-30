from flask import Blueprint, jsonify, request
from cerberus import Validator
from user.services import user as service
from user.validation.user import get_schema


user = Blueprint('user', __name__)


@user.route('/users', methods=['GET'])
def index():
    return jsonify(service.get())


@user.route('/users', methods=['POST'])
def create():
    v = Validator(get_schema())

    if v.validate(request.json):
        response = service.create(request.json)
        del response['password']

        return jsonify(response)
    else:
        return v.errors, 400


@user.route('/users/<user_id>', methods=['GET'])
def show(user_id):
    return jsonify(service.find({'_id': user_id}))


@user.route('/users/<user_id>', methods=['PUT'])
def update(user_id):
    v = Validator(get_schema())

    if v.validate(request.json):
        response = service.update({'_id': user_id}, request.json)
        del response['password']

        return jsonify(response)
    else:
        return v.errors, 400


@user.route('/users/<user_id>', methods=['DELETE'])
def delete(user_id):
    return jsonify(service.delete({'_id': user_id}))

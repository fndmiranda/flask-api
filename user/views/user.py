from flask import Blueprint, jsonify, request
from user.services import user as service


user = Blueprint('user', __name__)


@user.route('/users', methods=['GET'])
def index():
    return jsonify(service.get())


@user.route('/users', methods=['POST'])
def create():
    return jsonify(service.create(request.json))


@user.route('/users/<user_id>', methods=['GET'])
def show(user_id):
    return jsonify(service.find({'_id': user_id}))


@user.route('/users/<user_id>', methods=['PUT'])
def update(user_id):
    return jsonify(service.update({'_id': user_id}, request.json))


@user.route('/users/<user_id>', methods=['DELETE'])
def delete(user_id):
    return jsonify(service.delete({'_id': user_id}))

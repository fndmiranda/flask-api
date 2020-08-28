from flask import request, g, jsonify, current_app as app
from cerberus import Validator
from user.validations import user as validation
from user.services import UserService
from user.schemas import UserSchema, UsersPaginationSchema
from flask_smorest import Blueprint
from core.models import Session
from pprint import pprint
from marshmallow import ValidationError

schema = UserSchema()

session = Session()

blp = Blueprint(
    'users', 'users', url_prefix='/user/users',
    description='Operations on users'
)


@blp.route("", methods=["GET"])
@blp.response(
    schema=UsersPaginationSchema, description="List users.",
)
def list_users():
    """List users"""
    app.logger.info(
        'Starting list users with params: {} of request: {}'.format(
            request.values.to_dict(), g.request_id
        )
    )
    data = UserService().paginate()
    app.logger.info(
        'Response of list users with response: {} of request: {}'.format(
            {'meta': data.get('meta'), 'links': data.get('links')}, g.request_id
        )
    )
    return jsonify(data)


@blp.route("", methods=["POST"])
@blp.response(UserSchema, code=201)
def create_user():
    """Create user"""
    try:
        result = UserSchema().load(request.json)
        return jsonify(result)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # audit = request.json.copy()
    # audit.pop('password', None)

    # app.logger.info(
    #     'Starting create user with params: {} of request: {}'.format(audit, g.request_id)
    # )
    #
    # v = Validator(validation())
    #
    # if v.validate(request.json):
    #     data = schema.dump(UserService().create(request.json))
    #
    #     app.logger.info(
    #         'Response of create user with response: {} of request: {}'.format(data, g.request_id)
    #     )
    #
    #     return jsonify(data), 201
    # else:
    #     app.logger.info(
    #         'Response error of create user with response: {} of request: {}'.format(
    #             v.errors, g.request_id
    #         )
    #     )
    #     return jsonify(v.errors), 400


@blp.route("<user_id>", methods=["GET"])
@blp.response(UserSchema)
def get_user(user_id):
    """Get user by ID"""
    app.logger.info(
        'Starting show user id: {} of request: {}'.format(user_id, g.request_id)
    )

    response = schema.dump(UserService().find_or_404(user_id))

    app.logger.info(
        'Response of show user id: {} with response: {} of request: {}'.format(
            user_id, response, g.request_id
        )
    )
    return jsonify(response)


@blp.route("<user_id>", methods=["PUT"])
@blp.response(UserSchema)
def put_user(user_id):
    """Update user by ID"""
    app.logger.info(
        'Starting update user id: {} of request: {}'.format(user_id, g.request_id)
    )

    try:
        data = UserService().update_or_404(
            user_id, schema.load(request.json)
        )
        response = schema.dump(data)

        app.logger.info(
            'Response of update user id: {} with response: {} of request: {}'.format(
                user_id, response, g.request_id
            )
        )
        return jsonify(schema.dump(data))
    except ValidationError as err:
        app.logger.info(
            'Response error of update user id: {} with response: {} of request: {}'.format(
                user_id, err.messages, g.request_id
            )
        )
        return jsonify(err.messages), 400

    # audit = request.json.copy()
    # audit.pop('password', None)
    #
    # app.logger.info(
    #     'Starting update user with params: {} of request: {}'.format(audit, g.request_id)
    # )
    #
    # v = Validator(validation())
    #
    # if v.validate(request.json):
    #     data = schema.dump(UserService().update_or_404(user_id, request.json))
    #
        # app.logger.info(
        #     'Response of update user id: {} with response: {} of request: {}'.format(
        #         user_id, data, g.request_id
        #     )
        # )
    #
    #     return jsonify(data), 201
    # else:
    #     app.logger.info(
    #         'Response error of update user id: {} with response: {} of request: {}'.format(
    #             user_id, v.errors, g.request_id
    #         )
    #     )
    #     return jsonify(v.errors), 400


@blp.route("<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete user by ID"""
    app.logger.info(
        'Starting delete user id: {} of request: {}'.format(user_id, g.request_id)
    )

    UserService().delete_or_404(user_id)

    app.logger.info(
        'Response of user id: {} of request: {}'.format(user_id, g.request_id)
    )
    return {}, 204

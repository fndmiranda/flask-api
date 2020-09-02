from flask import g, jsonify, current_app as app
from user.services import UserService
from user.schemas import UserSchema, UserPaginationSchema
from core.schemas import QueryArgsSchema
from flask_smorest import Blueprint
from core.models import Session
from marshmallow import ValidationError
from auth import require_oauth

user_schema = UserSchema()

session = Session()

blp = Blueprint(
    'users', 'users', url_prefix='/user/users',
    description='Operations on users'
)


@blp.route('', methods=['GET'])
@blp.arguments(QueryArgsSchema, location='query')
@blp.response(
    schema=UserPaginationSchema, description="List users.",
)
@require_oauth()
def list_users(args):
    """List users"""
    app.logger.info(
        'Starting list users with args: {} of request: {}'.format(
            args, g.request_id
        )
    )

    data = UserService().paginate()
    app.logger.info(
        'Response of list users with response: {} of request: {}'.format(
            {'meta': data.get('meta'), 'links': data.get('links')}, g.request_id
        )
    )
    return jsonify(data)


@blp.route('', methods=['POST'])
@blp.arguments(user_schema)
@blp.response(user_schema, code=201)
@require_oauth()
def create_user(args):
    """Create user"""
    app.logger.info(
        'Starting create user of request: {}'.format(g.request_id)
    )
    try:
        values = user_schema.load(args)
        data = UserService().create(values)
        response = user_schema.dump(data)

        app.logger.info(
            'Response of create user with response: {} of request: {}'.format(
                response, g.request_id
            )
        )
        return jsonify(response), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@blp.route('<user_id>', methods=['GET'])
@blp.response(user_schema)
@require_oauth()
def get_user(user_id):
    """Get user by ID"""
    app.logger.info(
        'Starting show user id: {} of request: {}'.format(user_id, g.request_id)
    )

    response = user_schema.dump(UserService().find_or_404(user_id))

    app.logger.info(
        'Response of show user id: {} with response: {} of request: {}'.format(
            user_id, response, g.request_id
        )
    )
    return jsonify(response)


@blp.route('<user_id>', methods=['PUT'])
@blp.arguments(user_schema)
@blp.response(user_schema)
@require_oauth()
def put_user(args, user_id):
    """Update user by ID"""
    app.logger.info(
        'Starting update user id: {} of request: {}'.format(user_id, g.request_id)
    )

    try:
        values = user_schema.load(args)
        data = UserService().update_or_404(user_id, values)
        response = user_schema.dump(data)

        app.logger.info(
            'Response of update user id: {} with response: {} of request: {}'.format(
                user_id, response, g.request_id
            )
        )
        return jsonify(user_schema.dump(data))
    except ValidationError as err:
        app.logger.info(
            'Response error of update user id: {} with response: {} of request: {}'.format(
                user_id, err.messages, g.request_id
            )
        )
        return jsonify(err.messages), 400


@blp.route('<user_id>', methods=['DELETE'])
@blp.response(code=204)
@require_oauth()
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

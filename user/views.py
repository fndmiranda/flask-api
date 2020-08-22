from flask import request, g, current_app as app
from flask_restful import Resource
from cerberus import Validator
from user.validations import user as validation
from user.services import UserService
from user.schemas import UserSchema

schema = UserSchema()


class UserList(Resource):
    def get(self):
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
        return data

    def post(self):
        audit = request.json.copy()
        audit.pop('password', None)

        app.logger.info(
            'Starting create user with params: {} of request: {}'.format(audit, g.request_id)
        )

        v = Validator(validation())

        if v.validate(request.json):
            data = schema.dump(UserService().create(request.json))

            app.logger.info(
                'Response of create user with response: {} of request: {}'.format(data, g.request_id)
            )

            return data, 201
        else:
            app.logger.info(
                'Response error of create user with response: {} of request: {}'.format(
                    v.errors, g.request_id
                )
            )
            return v.errors, 400


class UserDetail(Resource):
    def get(self, user_id):
        app.logger.info(
            'Starting show user id: {} of request: {}'.format(user_id, g.request_id)
        )

        data = schema.dump(UserService().find_or_404(user_id))

        app.logger.info(
            'Response of show user id: {} with response: {} of request: {}'.format(
                user_id, data, g.request_id
            )
        )
        return data

    def delete(self, user_id):
        app.logger.info(
            'Starting delete user id: {} of request: {}'.format(user_id, g.request_id)
        )

        UserService().delete_or_404(user_id)

        app.logger.info(
            'Response of user id: {} of request: {}'.format(user_id, g.request_id)
        )
        return {}, 204

    def put(self, user_id):
        audit = request.json.copy()
        audit.pop('password', None)

        app.logger.info(
            'Starting update user with params: {} of request: {}'.format(audit, g.request_id)
        )

        v = Validator(validation())

        if v.validate(request.json):
            data = schema.dump(UserService().update_or_404(user_id, request.json))

            app.logger.info(
                'Response of update user id: {} with response: {} of request: {}'.format(
                    user_id, data, g.request_id
                )
            )

            return data, 201
        else:
            app.logger.info(
                'Response error of update user id: {} with response: {} of request: {}'.format(
                    user_id, v.errors, g.request_id
                )
            )
            return v.errors, 400

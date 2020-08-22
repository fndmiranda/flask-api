from flask import Flask, Blueprint
from flask_restful import Api
from authlib.integrations.flask_oauth2 import AuthorizationServer
from auth import query_client, save_token, require_oauth
from auth.views import bp as bp_auth_api
from auth.commands import bp as bp_auth_cli
from app.commands import bp as bp_app_cli
from user.commands import bp as bp_user_cli
from user.views import UserDetail, UserList
from authlib.oauth2.rfc6749 import grants
from auth.grants import PasswordGrant
from .interceptors import init_interceptors
from app.schema import ma


def create_app():
    """Construct the core application."""

    app = Flask(__name__)

    init_interceptors(app)
    app.config.from_pyfile('settings.py')

    ma.init_app(app)

    blueprint = Blueprint('api', __name__)
    api = Api(blueprint)

    api.add_resource(UserList, '/user/users')
    api.add_resource(UserDetail, '/user/users/<user_id>')

    app.register_blueprint(blueprint)
    app.register_blueprint(bp_auth_api)
    app.register_blueprint(bp_auth_cli)
    app.register_blueprint(bp_app_cli)
    app.register_blueprint(bp_user_cli)

    server = AuthorizationServer()

    # support all grants
    server.register_grant(grants.ImplicitGrant)
    server.register_grant(grants.ClientCredentialsGrant)
    server.register_grant(grants.AuthorizationCodeGrant)
    server.register_grant(PasswordGrant)
    server.register_grant(grants.RefreshTokenGrant)

    server.init_app(app, query_client=query_client, save_token=save_token)

    @app.route('/oauth/token', methods=['POST'])
    def issue_token():
        return server.create_token_response()

    @app.route('/', methods=['GET'])
    @require_oauth()
    def index():
        return {"hello": "world"}

    return app

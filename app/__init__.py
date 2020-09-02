import os
from importlib import resources
from flask import Flask, Blueprint
from authlib.integrations.flask_oauth2 import AuthorizationServer
from auth import query_client, save_token, require_oauth
from auth.views import bp as bp_auth_api
from auth.commands import bp as bp_auth_cli
from app.commands import bp as bp_app_cli
from user.commands import bp as bp_user_cli
from authlib.oauth2.rfc6749 import grants
from auth.grants import PasswordGrant
from .interceptors import init_interceptors
from app.schema import ma
from flask_smorest import Api, Blueprint
from flask_cors import CORS
from user.views import blp as blp_user
from flask_marshmallow import Marshmallow


def create_app():
    """Construct the core application."""

    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    init_interceptors(app)
    app.config.from_pyfile('settings.py')

    Marshmallow(app)

    blueprint = Blueprint('api', __name__)

    app.config['API_TITLE'] = 'My API'
    app.config['API_VERSION'] = "0.1.1"
    app.config['OPENAPI_VERSION'] = '3.0.3'

    app.config["OPENAPI_JSON_PATH"] = os.getenv("OPENAPI_JSON_PATH")
    app.config["OPENAPI_URL_PREFIX"] = os.getenv("OPENAPI_URL_PREFIX")
    app.config["OPENAPI_SWAGGER_UI_PATH"] = os.getenv("OPENAPI_SWAGGER_UI_PATH")
    app.config["OPENAPI_SWAGGER_UI_URL"] = os.getenv("OPENAPI_SWAGGER_UI_URL")
    app.config["OPENAPI_SWAGGER_UI_VERSION"] = os.getenv("OPENAPI_SWAGGER_UI_VERSION")
    app.config["OPENAPI_REDOC_PATH"] = os.getenv("OPENAPI_REDOC_PATH")
    app.config["OPENAPI_REDOC_URL"] = os.getenv("OPENAPI_REDOC_URL")

    app.config["API_SPEC_OPTIONS"] = {
        "info": {
            "title": "My API",
            "description": resources.read_text(__package__, "openapi.md")
        },
        "security": [{"bearerAuth": []}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Token JWT",
                },
            }
        },
    }

    api = Api(app)
    api.register_blueprint(blp_user)

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

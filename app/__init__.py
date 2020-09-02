import os
from importlib import resources
from flask import Flask, Blueprint
from auth import config_oauth, authorization
from auth import require_oauth
from auth.views import bp as bp_auth_api
from auth.commands import bp as bp_auth_cli
from app.commands import bp as bp_app_cli
from user.commands import bp as bp_user_cli
from .interceptors import init_interceptors
from app.schema import ma
from flask_smorest import Api, Blueprint
from flask_cors import CORS
from user.views import blp as blp_user
from flask_marshmallow import Marshmallow


def create_app():
    """Construct the core application."""

    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    init_interceptors(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    config_oauth(app)

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
        "security": [{"bearerAuth": []}, {"oauthAuth": []}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Token JWT",
                },
                "oauthAuth": {
                    "type": "oauth2",
                    "description": "This API uses OAuth 2 with the implicit grant flow.",
                    "flows": {
                        "password": {
                            "tokenUrl": "/oauth/token",
                            "refreshUrl": "/oauth/token",
                            "scopes": {
                                "read": "Grant read-only access to all your data except for the account and user info",
                                "write": "rant write-only access to all your data except for the account and user info",
                                "profile": "Grant read-only access to the account and user info only",
                            },
                        }
                    }
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

    @app.route('/', methods=['GET'])
    @require_oauth()
    def index():
        return {"hello": "world"}

    return app

from flask import Flask, Blueprint
from flask_restful import Api
from user.views import UserDetail, UserList


def create_app(config_filename):
    """Construct the core application."""

    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    blueprint = Blueprint('api', __name__)
    api = Api(blueprint)

    api.add_resource(UserList, '/user/users')
    api.add_resource(UserDetail, '/user/users/<user_id>')

    app.register_blueprint(blueprint)

    @app.route('/', methods=['GET'])
    def index():
        return {"hello": "world"}

    return app

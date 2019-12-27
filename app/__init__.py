from flask import Flask
from user.views.user import user
from app.database import get_db


def create_app(config_filename):
    """Construct the core application."""

    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    app.register_blueprint(user, url_prefix="/user")

    @app.route('/', methods=['GET'])
    def index():
        return {"hello": "world"}

    return app

from flask_pymongo import PyMongo
from flask import current_app, g


def get_db():
    if 'mongo' not in g:
        g.mongo = PyMongo()
        g.mongo.init_app(current_app)
    return g.mongo.db

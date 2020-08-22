import uuid
from flask import Flask, g


def before_request():
    if not hasattr(g, 'request_id'):
        setattr(g, 'request_id', uuid.uuid4())


def init_interceptors(app: Flask):
    app.before_request(before_request)

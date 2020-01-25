from decouple import config

SECRET_KEY = config('SECRET_KEY', default='secret', cast=str)
APP_NAME = config('APP_NAME', default='flask-api', cast=str)
FLASK_APP = config('FLASK_APP', default='app', cast=str)
FLASK_ENV = config('FLASK_ENV', default='production', cast=str)
DATABASE_URL = config('DATABASE_URL', default='sqlite:///database.sqlite', cast=str)
AUTHLIB_INSECURE_TRANSPORT = config('AUTHLIB_INSECURE_TRANSPORT', default=False, cast=bool)
OAUTH2_REFRESH_TOKEN_GENERATOR = config('OAUTH2_REFRESH_TOKEN_GENERATOR', default=True, cast=bool)

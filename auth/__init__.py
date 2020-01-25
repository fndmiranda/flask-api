from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from authlib.integrations.sqla_oauth2 import create_bearer_token_validator
from core.models import Session
from auth.models import Client, Token
from authlib.integrations.sqla_oauth2 import (
    create_query_client_func,
    create_save_token_func
)

session = Session()

query_client = create_query_client_func(session, Client)
save_token = create_save_token_func(session, Token)

require_oauth = ResourceProtector()
BearerTokenValidator = create_bearer_token_validator(session, Token)
require_oauth.register_token_validator(BearerTokenValidator())

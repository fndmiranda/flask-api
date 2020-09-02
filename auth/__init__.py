from authlib.integrations.sqla_oauth2 import create_revocation_endpoint
from .grants import PasswordGrant
from auth.models import AuthorizationCode
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from authlib.integrations.sqla_oauth2 import create_bearer_token_validator
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7636 import CodeChallenge
from core.models import Session
from auth.models import Client, Token
from authlib.integrations.sqla_oauth2 import (
    create_query_client_func,
    create_save_token_func
)

session = Session()

query_client = create_query_client_func(session, Client)
save_token = create_save_token_func(session, Token)
authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token,
)
require_oauth = ResourceProtector()


def config_oauth(app):
    authorization.init_app(app, query_client=query_client, save_token=save_token)

    # support all grants
    authorization.register_grant(grants.ImplicitGrant)
    authorization.register_grant(grants.ClientCredentialsGrant)
    authorization.register_grant(grants.AuthorizationCodeGrant)
    authorization.register_grant(PasswordGrant)
    authorization.register_grant(grants.RefreshTokenGrant)

    # support revocation
    revocation_cls = create_revocation_endpoint(session, Token)
    authorization.register_endpoint(revocation_cls)

    # protect resource
    bearer_cls = create_bearer_token_validator(session, Token)
    require_oauth.register_token_validator(bearer_cls())

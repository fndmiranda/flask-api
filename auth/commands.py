import click
import time
from flask import Blueprint
from werkzeug.security import gen_salt
from app import settings
from auth.services import ClientService

bp = Blueprint('auth', __name__)


@bp.cli.command('client:create')
@click.option('--name')
@click.option('--user')
@click.option('--uri')
@click.option('--grant_type')
@click.option('--redirect')
@click.option('--response')
@click.option('--scope')
def client_create(name, user, uri, grant_type, redirect, response, scope):
    """Create a new OAuth2 client."""
    data = {
        'client_name': name if name else settings.APP_NAME,
        'client_uri': uri,
        'user_id': user,
        'grant_types': grant_type.split(',') if grant_type is not None else ['password'],
        'redirect_uris': redirect.split(',') if redirect is not None else None,
        'response_types': response.split(',') if response is not None else ['code'],
        'scope': scope,
        'token_endpoint_auth_method': 'client_secret_post',
        'client_id': gen_salt(24),
        'client_id_issued_at': int(time.time()),
        'client_secret': gen_salt(48),
    }

    client = ClientService().create(data)

    print("\033[1;32;48m{}".format('New OAuth2 client created successfully.'))
    print("\033[0;33;48m{}".format('Client ID:'), "\033[0;37;48m{}".format(client.client_id))
    print("\033[0;33;48m{}".format('Client secret:'), "\033[0;37;48m{}".format(client.client_secret))
    print("\033[0;33;48m{}".format('Grant type:'), "\033[0;37;48m{}".format(client.client_metadata['grant_types']))

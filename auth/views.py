import time
from flask import request
from flask_smorest import Blueprint
from flask import render_template, redirect
from werkzeug.security import gen_salt
from core.models import Session
from auth.models import Client
from . import authorization

bp = Blueprint(
    'oauth', 'oauth', url_prefix='/oauth',
    description='Operations on oauth'
)


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]


@bp.route('/create_client', methods=('GET', 'POST'))
def create_client():
    session = Session()
    if request.method == 'GET':
        return render_template('create_client.html')

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
    )

    if client.token_endpoint_auth_method == 'none':
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)

    form = request.form
    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form["client_uri"],
        "grant_types": split_by_crlf(form["grant_type"]),
        "redirect_uris": split_by_crlf(form["redirect_uri"]),
        "response_types": split_by_crlf(form["response_type"]),
        "scope": form["scope"],
        "token_endpoint_auth_method": form["token_endpoint_auth_method"]
    }
    client.set_client_metadata(client_metadata)
    session.add(client)
    session.commit()
    return redirect('/')


@bp.route('/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')

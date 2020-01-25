import time
from core.services import BaseService
from werkzeug.security import gen_salt
from auth.repositories import ClientRepository
from core.models import Session


class ClientService(BaseService):
    """Class representing the product service."""

    _repository = ClientRepository

    def create(self, payload):
        """Save a new register."""
        session = Session()

        client = self.get_repository().make(
            client_id=gen_salt(24),
            client_secret=gen_salt(48),
            client_id_issued_at=int(time.time()),
            user_id=payload['user_id']
        )

        client_metadata = {
            "client_name": payload['client_name'],
            "client_uri": payload['client_uri'],
            "grant_types": payload['grant_types'],
            "redirect_uris": payload['redirect_uris'],
            "response_types": payload['response_types'],
            "scope": payload['scope'],
            "token_endpoint_auth_method": payload['token_endpoint_auth_method']
        }

        client.set_client_metadata(client_metadata)

        session.add(client)
        session.commit()

        return client

from auth.models import Client
from core.repositories import BaseRepository


class ClientRepository(BaseRepository):
    """Class representing the product repository."""

    _model = Client

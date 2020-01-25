from user.repositories import UserRepository
from core.services import BaseService
import crypt


class UserService(BaseService):
    """Class representing the product service."""

    _repository = UserRepository

    def update(self, pk, payload):
        """Update a register."""
        return self.get_repository().update(pk, self._prepare(payload))

    def create(self, payload):
        """Save a new register."""
        return self.get_repository().create(self._prepare(payload))

    @staticmethod
    def _prepare(payload):
        """Prepare payload to save."""
        if 'password' in payload:
            payload['password'] = crypt.crypt(payload['password'])
        return payload

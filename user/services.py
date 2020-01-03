from user.repositories import UserRepository
from core.services import BaseService


class UserService(BaseService):
    """Class representing the product service."""

    _repository = UserRepository

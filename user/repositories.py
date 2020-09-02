from user.models import User
from user.schemas import UserSchema
from core.repositories import BaseRepository


class UserRepository(BaseRepository):
    """Class representing the product repository."""

    _model = User
    _schema = UserSchema

import crypt
import sqlalchemy as sa
from core.models import Base
from core.models import ModelMixin, TimestampMixin
from hmac import compare_digest as compare_hash


class User(Base, ModelMixin, TimestampMixin):
    __tablename__ = 'user_users'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), nullable=False, unique=True)
    password = sa.Column(sa.String(255), nullable=False)
    is_admin = sa.Column(sa.Boolean(), nullable=False, default=False)

    def get_user_id(self):
        return self.id

    def check_password(self, password):
        return compare_hash(crypt.crypt(password, self.password), self.password)

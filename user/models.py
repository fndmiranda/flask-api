import crypt
from sqlalchemy import Column, Integer, String
from core.models import Base
from core.models import ModelMixin, TimestampMixin
from hmac import compare_digest as compare_hash


class User(Base, ModelMixin, TimestampMixin):
    __tablename__ = 'user_users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    def get_user_id(self):
        return self.id

    def check_password(self, password):
        return compare_hash(crypt.crypt(password, self.password), self.password)

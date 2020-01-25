import time
from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin, OAuth2TokenMixin, OAuth2AuthorizationCodeMixin
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.models import Base, ModelMixin


class Client(Base, ModelMixin, OAuth2ClientMixin):
    __tablename__ = 'oauth_clients'

    user_id = Column(Integer, ForeignKey('user_users.id', ondelete='CASCADE'))
    user = relationship('User')


class Token(Base, ModelMixin, OAuth2TokenMixin):
    __tablename__ = 'oauth_tokens'

    user_id = Column(Integer, ForeignKey('user_users.id', ondelete='CASCADE'))
    user = relationship('User')

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()


class AuthorizationCode(Base, ModelMixin, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth_codes'

    user_id = Column(Integer, ForeignKey('user_users.id', ondelete='CASCADE'))
    user = relationship('User')

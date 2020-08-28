from authlib.oauth2.rfc6749 import grants
from user.services import UserService
from user.models import User


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = ['client_secret_post']

    def authenticate_user(self, username, password):
        user = UserService().filter(User.email == username)
        if user.check_password(password):
            return user

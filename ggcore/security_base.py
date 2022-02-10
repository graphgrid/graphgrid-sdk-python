import base64
from dataclasses import dataclass

from ggcore.credentials import Credentials

AUTH_HEADER_KEY = "Authorization"
BASIC_HEADER_KEY = "Basic"
BEARER_HEADER_KEY = "Bearer"

GRANT_TYPE_KEY = "grant_type"
PASSWORD_KEY = "password"
USERNAME_KEY = "username"

@dataclass
class RequestAuth():
    credentials: Credentials

    def get_auth_headers(self):
        pass


class BasicAuth(RequestAuth):

    def get_auth_headers(self):
        key_secret_string = f'{self.credentials.access_key}:{self.credentials.secret_key}'
        b64_encoded_basic_auth = base64.b64encode(f'{key_secret_string}'.encode())

        return {AUTH_HEADER_KEY: f'{BASIC_HEADER_KEY} {b64_encoded_basic_auth}'}


class BearerAuth(RequestAuth):

    def get_auth_headers(self):
        return {AUTH_HEADER_KEY: f'{BEARER_HEADER_KEY} {self.credentials.token}'}

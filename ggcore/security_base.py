import base64
import enum
from dataclasses import dataclass

from ggcore import sdk_exceptions
from ggcore.credentials import Credentials

AUTH_HEADER_KEY = "Authorization"
BASIC_HEADER_KEY = "Basic"
BEARER_HEADER_KEY = "Bearer"

GRANT_TYPE_KEY = "grant_type"
PASSWORD_KEY = "password"
USERNAME_KEY = "username"


class RequestAuthType(enum.Enum):
    BASIC = BASIC_HEADER_KEY
    BEARER = BEARER_HEADER_KEY


@dataclass
class RequestAuth:
    credentials: Credentials

    def get_auth_header(self):
        pass


@dataclass
class RequestAuthFactory:

    @classmethod
    def from_auth_type(cls, request_type: RequestAuthType, credentials: Credentials) -> RequestAuth:
        if request_type == request_type.BASIC:
            return BasicAuth(credentials)
        elif request_type == request_type.BEARER:
            return BearerAuth(credentials)
        raise sdk_exceptions.SdkBadAuthTypeException()


@dataclass
class BasicAuth(RequestAuth):

    def get_auth_header(self):
        key_secret_string = f'{self.credentials.access_key}:{self.credentials.secret_key}'
        b64_encoded_basic_auth = base64.b64encode(f'{key_secret_string}'.encode())

        return {AUTH_HEADER_KEY: f'{BASIC_HEADER_KEY} {b64_encoded_basic_auth.decode()}'}


@dataclass
class BearerAuth(RequestAuth):

    def get_auth_header(self):
        return {AUTH_HEADER_KEY: f'{BEARER_HEADER_KEY} {self.credentials.token}'}


@dataclass
class SdkAuth():
    credentials: Credentials

    def get_auth(self, auth_type: RequestAuthType):
        return RequestAuthFactory.from_auth_type(auth_type, self.credentials).get_auth_header()

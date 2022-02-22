import base64
from dataclasses import dataclass

from ggcore import sdk_exceptions
from ggcore.credentials import Credentials
from ggcore.utils import AUTH_HEADER_KEY, BASIC_HEADER_KEY, BEARER_HEADER_KEY, RequestAuthType


@dataclass
class RequestAuth:
    credentials: Credentials

    def get_auth_header(self) -> dict:
        pass


class RequestAuthFactory:
    @classmethod
    def from_auth_type(cls, request_type: RequestAuthType, credentials: Credentials) -> RequestAuth:
        if request_type == request_type.BASIC:
            return BasicAuth(credentials)
        elif request_type == request_type.BEARER:
            return BearerAuth(credentials)
        raise sdk_exceptions.SdkAuthTypeException()


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
class SdkAuth:
    credentials: Credentials

    def get_auth_for_http(self, auth_type: RequestAuthType) -> dict:
        return RequestAuthFactory.from_auth_type(auth_type, self.credentials).get_auth_header()

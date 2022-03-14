import base64
from dataclasses import dataclass

from ggcore.config import SdkSecurityConfig
from ggcore.utils import AUTH_HEADER_KEY, BASIC_HEADER_KEY, BEARER_HEADER_KEY


@dataclass
class RequestAuth:
    security_config: SdkSecurityConfig

    def get_auth_value(self) -> str:
        pass

    def get_auth_key(self) -> str:
        pass

    def get_auth_header(self) -> dict:
        return {
            AUTH_HEADER_KEY: f'{self.get_auth_key()} {self.get_auth_value()}'}


@dataclass
class BasicAuth(RequestAuth):
    def get_auth_value(self) -> str:
        key_secret_string = f'{self.security_config.access_key}:{self.security_config.secret_key}'
        b64_encoded_basic_auth = base64.b64encode(
            f'{key_secret_string}'.encode())
        return b64_encoded_basic_auth.decode()

    def get_auth_key(self) -> str:
        return BASIC_HEADER_KEY


@dataclass
class BearerAuth(RequestAuth):
    def get_auth_value(self) -> str:
        return self.security_config.token

    def get_auth_key(self) -> str:
        return BEARER_HEADER_KEY


class SdkAuthHeaderBuilder:
    @classmethod
    def get_basic_header(self, sec_conf: SdkSecurityConfig) -> dict:
        return BasicAuth(sec_conf).get_auth_header()

    @classmethod
    def get_bearer_header(self, sec_conf: SdkSecurityConfig) -> dict:
        return BearerAuth(sec_conf).get_auth_header()

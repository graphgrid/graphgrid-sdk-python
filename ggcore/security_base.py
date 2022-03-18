"""Define classes for request auth and building auth headers."""

import base64
from dataclasses import dataclass

from ggcore.config import SdkSecurityConfig
from ggcore.utils import AUTH_HEADER_KEY, BASIC_HEADER_KEY, BEARER_HEADER_KEY


@dataclass
class RequestAuth:
    """Define base class for the different request auth types."""
    security_config: SdkSecurityConfig

    def get_auth_value(self) -> str:
        """Return the authentication value."""

    def get_auth_key(self) -> str:
        """Return the authentication key."""

    def get_auth_header(self) -> dict:
        """Build and return the authentication header."""
        return {
            AUTH_HEADER_KEY: f'{self.get_auth_key()} {self.get_auth_value()}'}


@dataclass
class BasicAuth(RequestAuth):
    """Define class to form headers for Basic auth."""

    def get_auth_value(self) -> str:
        key_secret_string = f'{self.security_config.access_key}:' \
                            f'{self.security_config.secret_key}'

        b64_encoded_basic_auth = base64.b64encode(
            f'{key_secret_string}'.encode())
        return b64_encoded_basic_auth.decode()

    def get_auth_key(self) -> str:
        return BASIC_HEADER_KEY


@dataclass
class BearerAuth(RequestAuth):
    """Define class to form headers for Bearer auth."""

    def get_auth_value(self) -> str:
        return self.security_config.token

    def get_auth_key(self) -> str:
        return BEARER_HEADER_KEY


class SdkAuthHeaderBuilder:
    """Define class to get specific auth headers based on security
    config.
    """

    @classmethod
    def get_basic_header(cls, sec_conf: SdkSecurityConfig) -> dict:
        """Return the basic auth for the provided security config."""
        return BasicAuth(sec_conf).get_auth_header()

    @classmethod
    def get_bearer_header(cls, sec_conf: SdkSecurityConfig) -> dict:
        """Return the bearer auth for the provided security config."""
        return BearerAuth(sec_conf).get_auth_header()

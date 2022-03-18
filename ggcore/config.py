"""Define classes and constants for controlling sdk configuration."""

import typing
from dataclasses import dataclass

URL_BASE = "URL_BASE"
OAUTH_CLIENT_ID = "OAUTH_CLIENT_ID"
OAUTH_CLIENT_SECRET = "OAUTH_CLIENT_SECRET"

BOOTSTRAP_CONFIG_KEYS = [URL_BASE,
                         OAUTH_CLIENT_ID,
                         OAUTH_CLIENT_SECRET, ]


@dataclass
class SdkBootstrapConfig:
    """Define class representing bootstrap sdk configuration."""
    url_base: typing.AnyStr
    access_key: typing.AnyStr
    secret_key: typing.AnyStr


# pylint: disable=too-few-public-methods
class SdkSecurityConfig(SdkBootstrapConfig):
    """Define class representing Security base sdk configuration."""
    _token: typing.AnyStr = None

    def __init__(self, bootstrap_config: SdkBootstrapConfig, token=None):
        super().__init__(bootstrap_config.url_base, bootstrap_config.access_key,
                         bootstrap_config.secret_key)
        self._token = token

    # pylint: disable=missing-function-docstring
    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

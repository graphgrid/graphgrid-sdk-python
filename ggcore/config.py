import typing
from dataclasses import dataclass

URL_BASE = "URL_BASE"  # rename/revalue to SERVICE_BASE ?
OAUTH_CLIENT_ID = "OAUTH_CLIENT_ID"
OAUTH_CLIENT_SECRET = "OAUTH_CLIENT_SECRET"

BOOTSTRAP_CONFIG_KEYS = [URL_BASE,
                         OAUTH_CLIENT_ID,
                         OAUTH_CLIENT_SECRET, ]


@dataclass
class SdkBootstrapConfig:
    url_base: typing.AnyStr
    access_key: typing.AnyStr
    secret_key: typing.AnyStr


class SdkSecurityConfig(SdkBootstrapConfig):
    _token: typing.AnyStr = None

    def __init__(self, bootstrap_config: SdkBootstrapConfig, token=None):
        super().__init__(bootstrap_config.url_base, bootstrap_config.access_key, bootstrap_config.secret_key)
        self._token = token

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

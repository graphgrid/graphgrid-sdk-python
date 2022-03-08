import typing
from dataclasses import dataclass

from ggcore.credentials import Credentials

URL_BASE = "URL_BASE"  # rename/revalue to SERVICE_BASE ?
OAUTH_CLIENT_ID = "OAUTH_CLIENT_ID"
OAUTH_CLIENT_SECRET = "OAUTH_CLIENT_SECRET"

BOOTSTRAP_CONFIG_KEYS = [URL_BASE,
                         OAUTH_CLIENT_ID,
                         OAUTH_CLIENT_SECRET, ]


@dataclass
class SecurityConfig:
    url_base: typing.AnyStr
    access_key: typing.AnyStr
    secret_key: typing.AnyStr

    def __post_init__(self):
        self.credentials = Credentials(self.access_key, self.secret_key)

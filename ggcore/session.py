from ggcore.config import SdkConfig
from ggcore.credentials import Credentials


class SessionCore:
    _credentials: Credentials = None
    _config: SdkConfig

    # def __init__(self):
    #     pass

    def module(self):
        pass

    def set_credentials(self, access_key, secret_key, token=None):
        self._credentials = Credentials(access_key, secret_key, token)


def get_session(env_vars=None):
    return SessionCore(env_vars)

from ggcore.config import SdkConfig
from ggcore.credentials import Credentials
from ggcore.sdk_exceptions import SdkInvalidConfigKey


class SessionCore:
    _credentials: Credentials = None
    _config: SdkConfig

    def set_credentials(self, access_key, secret_key, token=None):
        self._credentials = Credentials(access_key, secret_key, token)

    def get_config(self, key):
        if key in self._config:
            return self._config[key]
        else:
            raise SdkInvalidConfigKey

    @property
    def credentials(self):
        return self._credentials


def get_session(env_vars=None):
    return SessionCore(env_vars)

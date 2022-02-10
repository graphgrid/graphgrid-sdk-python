import ggcore.credentials


class SessionCore:

    def __init__(self,):
        self._credentials = None

    def create_client(self):
        pass

    def set_credentials(self, access_key, secret_key, token=None):
        self._credentials = ggcore.credentials.Credentials(access_key, secret_key, token)

def get_session(env_vars=None):
    return SessionCore(env_vars)
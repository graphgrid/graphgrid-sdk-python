from ggcore.credentials import Credentials


class GraphGridSession:
    """
    GraphGridSession used to
    """
    _credentials: Credentials

    def __init__(self, access_key, secret_access_key):
        self._credentials = Credentials(access_key, secret_access_key)

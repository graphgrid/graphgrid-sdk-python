import typing

import ggcore.client_factory
from ggcore.client import GraphGridModuleClient
from ggcore.credentials import Credentials


class GraphGridSession:
    """

    """
    _credentials: Credentials
    _client_map: typing.Dict[str, GraphGridModuleClient]

    def __init__(self, access_key, secret_access_key):
        self._credentials = Credentials(access_key, secret_access_key)

    def client(self, name) -> GraphGridModuleClient:
        self._client_map[name] = ggcore.client_factory.client(name)
        return self._client_map[name]

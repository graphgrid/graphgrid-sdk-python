import typing

import ggcore.client_factory
from ggcore.client import GraphGridModuleClient, NlpClient
from ggcore.credentials import Credentials
from ggcore.utils import NLP


class GraphGridSession:
    """

    """
    _credentials: Credentials
    _client_map: typing.Dict[str, GraphGridModuleClient]

    def __init__(self, access_key, secret_access_key):
        self._credentials = Credentials(access_key, secret_access_key)

    def client(self, name: str) -> GraphGridModuleClient:
        if name not in self._client_map:
            self._client_map[name] = ggcore.client_factory.client(name)
        return self._client_map[name]

    def saveDataset(self):
        """
        Work in progress
        """
        nlp_client: NlpClient = self.client(NLP)
        nlp_client.save()

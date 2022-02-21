import typing

import ggcore.client_factory
from ggcore.client import GraphGridModuleClient, SecurityClient
from ggcore.credentials import Credentials
from ggcore.utils import CONFIG, SECURITY


class GraphGridSession:
    """

    """
    _url_base: str
    _credentials: Credentials
    _client_map: typing.Dict[str, GraphGridModuleClient]

    def __init__(self, access_key, secret_access_key, url_base="localhost"):
        self._url_base = url_base
        self._credentials = Credentials(access_key, secret_access_key)
        self._client_map = {}

    # def __init__(self, credentials: Credentials):
    #     self._credentials = credentials

    def client(self, name: str) -> GraphGridModuleClient:
        if name not in self._client_map:
            self._client_map[name] = ggcore.client_factory.client(name, self._url_base)
        return self._client_map[name]

    #
    # def save_dataset(self):
    #     """
    #     Work in progress
    #     """
    #     nlp_client: NlpClient = self.client(NLP)
    #     nlp_client.save()
    #     pass

    def setup_config_client(self):
        self.client(CONFIG)

    def setup_security_client(self):
        self.client(SECURITY)

        security_client: SecurityClient = self.client(SECURITY)

        self._credentials.token = security_client.get_token(self._credentials)

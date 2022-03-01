import typing

import ggcore.client_factory
from ggcore.client import GraphGridModuleClient, SecurityClient, ConfigClient
from ggcore.credentials import Credentials
from ggcore.session import SessionCore
from ggcore.utils import SECURITY, CONFIG

"""
example sdk usage?
    sdk = GraphGridSdk()
    
    sdk.save( "path/to/dataset" )
    
    sdk.
"""


class GraphGridSdk:
    """

    """
    _url_base: str
    _credentials: Credentials

    _client_map: typing.Dict[str, GraphGridModuleClient]
    _session: SessionCore

    def __init__(self, access_key, secret_access_key, url_base="localhost"):
        self._url_base = url_base
        self._credentials = Credentials(access_key, secret_access_key)
        self._client_map = {}

        self.setup_clients()

        self.setup_session()


    def setup_session(self):
        self._session.set_credentials(self._credentials)
        # self._session.setup

    def setup_clients(self):
        self._setup_config_client()
        self._setup_security_client()

    def _client(self, name: str) -> GraphGridModuleClient:
        if name not in self._client_map:
            self._client_map[name] = ggcore.client_factory.client(name)
        return self._client_map[name]

    def _setup_config_client(self):
        config_client: ConfigClient = self._client(CONFIG)

    def _setup_security_client(self):
        security_client: SecurityClient = self._client(SECURITY)

    def save_dataset(self):
        pass

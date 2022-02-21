import typing

import ggcore.client_factory
from ggcore.client import GraphGridModuleClient, SecurityClient, ConfigClient
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

        self.setup_config_client()
        self.setup_security_client()

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
        config_client: ConfigClient = self.client(CONFIG)
        # need to get url_base from here?
        # is there anyway this needs to call config before it can call security client? Is the config client technically needed?

    def setup_security_client(self):
        security_client: SecurityClient = self.client(SECURITY)
        self._credentials.token = security_client.get_token(self._credentials)


        # need to take care of refresh token so security creds are completely handled on in the background without
        # the user having to know about getting a token/when that token expires. It should "just work"

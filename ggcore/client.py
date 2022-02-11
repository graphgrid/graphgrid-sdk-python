from dataclasses import dataclass

from ggcore.utils import CONFIG, NLP, SECURITY


@dataclass
class GraphGridModuleClient:
    def is_available(self):
        pass

    def client_name(self):
        pass


@dataclass
class ConfigClient(GraphGridModuleClient):
    _client_name = CONFIG

    @property
    def client_name(self):
        return self._client_name


class SecurityClient(GraphGridModuleClient):
    _client_name = SECURITY

    @property
    def client_name(self):
        return self._client_name


class NlpClient(GraphGridModuleClient):
    _client_name = NLP

    @property
    def client_name(self):
        return self._client_name

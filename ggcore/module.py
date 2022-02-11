from dataclasses import dataclass

from ggcore.utils import CONFIG, NLP, SECURITY


@dataclass
class ModuleClient:
    def is_available(self):
        pass

    @property
    def client_name(self):
        pass


@dataclass
class ConfigClient(ModuleClient):
    _client_name = CONFIG

    @property
    def client_name(self):
        return self._client_name


class SecurityClient(ModuleClient):
    _client_name = SECURITY

    @property
    def client_name(self):
        return self._client_name


class NlpClient(ModuleClient):
    _client_name = NLP

    @property
    def client_name(self):
        return self._client_name

import enum
from dataclasses import dataclass

from ggcore.client import ConfigClient, SecurityClient, NlpClient
from ggcore.utils import CONFIG, SECURITY, NLP


@dataclass
class GraphGridClientFactory:
    def create_client_instance(self):
        pass


class ConfigClientFactory(GraphGridClientFactory):
    def create_client_instance(self):
        return ConfigClient()


class SecurityClientFactory(GraphGridClientFactory):
    def create_client_instance(self):
        return SecurityClient()


class NlpClientFactory(GraphGridClientFactory):
    def create_client_instance(self):
        return NlpClient()


class ClientFactory(enum.Enum):
    config = CONFIG
    security = SECURITY
    nlp = NLP

    _factory: GraphGridClientFactory

    def __init__(self, value):
        super().__init__()

        factory_map = {
            CONFIG: ConfigClientFactory,
            SECURITY: SecurityClientFactory,
            NLP: NlpClientFactory,
        }
        if self.value in factory_map:
            self._factory = factory_map[self.value]()

    def create_client(self):
        return self._factory.create_client_instance()


def client(s: str):
    return ClientFactory(s).create_client()

import enum
from dataclasses import dataclass

from ggcore.module import ConfigClient, SecurityClient, NlpClient

CONFIG = 'config'
SECURITY = 'security'
NLP = 'nlp'


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


class SessionFactoryFactory(enum.Enum):
    config = CONFIG
    security = SECURITY
    nlp = NLP

    _factory: GraphGridClientFactory

    def __init__(self, value):
        super().__init__()

        options = {
            CONFIG: self._config,
            SECURITY: self._security,
            NLP: self._nlp,
        }
        if self.value in options:
            self._factory = options[self.value]()
        else:
            raise Exception("bad module str")

    def _config(self):
        return ConfigClientFactory()

    def _security(self):
        return SecurityClientFactory()

    def _nlp(self):
        return NlpClientFactory()

    def create_client(self):
        return self._factory.create_client_instance()


def client(s: str):
    return SessionFactoryFactory(s).create_client()

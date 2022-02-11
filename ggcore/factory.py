import enum
from dataclasses import dataclass

from ggcore.module import ConfigModuleSession, SecurityModuleSession, NlpModuleSession

CONFIG = 'config'
SECURITY = 'security'
NLP = 'nlp'


@dataclass
class GraphGridModuleFactory:
    def create_module_instance(self):
        pass


class ConfigModuleFactory(GraphGridModuleFactory):
    def __init__(self, ):
        print("config fact")

    def create_module_instance(self):
        return ConfigModuleSession()


class SecurityModuleFactory(GraphGridModuleFactory):
    def __init__(self, ):
        print("sec fact")

    def create_module_instance(self):
        return SecurityModuleSession()


class NlpModuleFactory(GraphGridModuleFactory):
    def __init__(self, ):
        print("nlp factory")

    def create_module_instance(self):
        return NlpModuleSession()


class ModuleFactoryFactory(enum.Enum):
    config = CONFIG
    security = SECURITY
    nlp = NLP

    _factory: GraphGridModuleFactory

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
        return ConfigModuleFactory()

    def _security(self):
        return SecurityModuleFactory()

    def _nlp(self):
        return NlpModuleFactory()

    def create_module(self):
        return self._factory.create_module_instance()


def module(s: str):
    return ModuleFactoryFactory(s).create_module()

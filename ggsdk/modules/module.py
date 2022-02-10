import enum
import typing
from dataclasses import dataclass

CONFIG = 'config'
SECURITY = 'security'
NLP = 'nlp'


@dataclass
class GraphGridModuleFactory:
    def create_module_instance(self):
        pass


@dataclass
class GraphGridModule:
    def is_available(self):
        pass


class ConfigModule(GraphGridModule):
    def __init__(self, ):
        print("CONFIG SDK MODULE CREATED")


class NlpModule(GraphGridModule):
    def __init__(self, ):
        print("NLP SDK MODULE CREATED")


class SecurityModule(GraphGridModule):
    def __init__(self, ):
        print("SECURITY SDK MODULE CREATED")


class ConfigModuleFactory(GraphGridModuleFactory):
    def __init__(self, ):
        print("config fact")

    def create_module_instance(self):
        return ConfigModule()


class SecurityModuleFactory(GraphGridModuleFactory):
    def __init__(self, ):
        print("sec fact")

    def create_module_instance(self):
        return SecurityModule()


class NlpModuleFactory(GraphGridModuleFactory):
    def __init__(self, ):
        print("nlp factory")

    def create_module_instance(self):
        return NlpModule()


class ModuleFactoryFactory(enum.Enum):
    config = CONFIG
    security = SECURITY
    nlp = NLP

    _factory: GraphGridModuleFactory

    def __init__(self, value):
        super().__init__()

        options = {
            CONFIG: self._config(),
            SECURITY: self._security(),
            NLP: self._nlp(),
        }
        if self.value in options:
            self._factory = options[self.value]
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

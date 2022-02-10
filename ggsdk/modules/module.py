import enum
import typing
from dataclasses import dataclass

CONFIG = 'config'
SECURITY = 'security'
NLP = 'nlp'


@dataclass
class GraphGridModuleFactory:
    pass


@dataclass
class GraphGridModule:
    def is_available(self):
        pass



class ConfigModuleFactory(GraphGridModuleFactory):
    def __init__(self,):
        print(CONFIG + "1")



class SecurityModuleFactory(GraphGridModuleFactory):
    def __init__(self,):
        print(SECURITY)



class NlpModuleFactory(GraphGridModuleFactory):
    def __init__(self,):
        print(NLP)


class ModuleFactoryFactory(enum.Enum):
    config = CONFIG
    security = SECURITY
    nlp = NLP

    def __init__(self, value):
        options = {
            CONFIG: self._config,
            SECURITY: self._security,
            NLP: self._nlp
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

    def factory(self):
        return self._factory

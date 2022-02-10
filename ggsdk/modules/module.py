import enum
import typing
from dataclasses import dataclass


class ModuleType(enum.Enum):
    config = 0
    security = 1
    nlp = 2

@dataclass
class GraphGridModule:
    module_type: typing.Any[ModuleType]

    def is_available(self):
        pass


@dataclass
class GraphGridModuleFactory:
    pass

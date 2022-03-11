import typing
from dataclasses import dataclass

from ggcore import sdk_exceptions
from ggcore.client import ConfigClient, SecurityClient, NlpClient, ClientBase
from ggcore.utils import CONFIG, SECURITY, NLP


# todo remove this file? tempted to keep it around for the future

class GraphGridModuleClientFactory:
    def create_client_instance(self) -> ClientBase:
        pass


class ConfigClientFactory(GraphGridModuleClientFactory):
    def create_client_instance(self) -> ClientBase:
        return ConfigClient()


class SecurityClientFactory(GraphGridModuleClientFactory):
    def create_client_instance(self) -> ClientBase:
        return SecurityClient()


class NlpClientFactory(GraphGridModuleClientFactory):
    def create_client_instance(self) -> ClientBase:
        return NlpClient()


@dataclass
class FactoryData:
    client_name: str
    factory: GraphGridModuleClientFactory


class ClientFactory:
    _FACTORIES_DATA: typing.Dict[str, FactoryData] = {
        CONFIG: FactoryData(CONFIG, ConfigClientFactory()),
        SECURITY: FactoryData(SECURITY, SecurityClientFactory()),
        NLP: FactoryData(NLP, NlpClientFactory()),
    }

    @classmethod
    def call_module_client_factory(cls, validated_client_name) -> ClientBase:
        return cls._FACTORIES_DATA.get(validated_client_name).factory.create_client_instance()

    @classmethod
    def create_client(cls, client_name) -> ClientBase:
        if client_name in cls._FACTORIES_DATA:
            return cls.call_module_client_factory(client_name)
        else:
            raise sdk_exceptions.SdkInvalidClient


def client(s: str) -> ClientBase:
    return ClientFactory.create_client(s)

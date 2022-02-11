import typing
from dataclasses import dataclass

from ggcore import sdk_exceptions
from ggcore.client import ConfigClient, SecurityClient, NlpClient, GraphGridModuleClient
from ggcore.utils import CONFIG, SECURITY, NLP


@dataclass
class GraphGridClientFactory:
    def create_client_instance(self) -> GraphGridModuleClient:
        pass


class ConfigClientFactory(GraphGridClientFactory):
    def create_client_instance(self) -> GraphGridModuleClient:
        return ConfigClient()


class SecurityClientFactory(GraphGridClientFactory):
    def create_client_instance(self) -> GraphGridModuleClient:
        return SecurityClient()


class NlpClientFactory(GraphGridClientFactory):
    def create_client_instance(self) -> GraphGridModuleClient:
        return NlpClient()


@dataclass
class FactoryData:
    client_name: str
    factory: typing.Type[GraphGridClientFactory]


class ClientFactory:
    _FACTORIES_DATA: typing.Dict[str, FactoryData] = {
        CONFIG:     FactoryData(CONFIG, ConfigClientFactory),
        SECURITY:   FactoryData(SECURITY, SecurityClientFactory),
        NLP:        FactoryData(NLP, NlpClientFactory),
    }

    @classmethod
    def call_module_client_factory(cls, validated_client_name):
        return cls._FACTORIES_DATA.get(validated_client_name).factory().create_client_instance()

    @classmethod
    def create_client(cls, client_name):
        if client_name in cls._FACTORIES_DATA:
            return cls.call_module_client_factory(client_name)
        else:
            raise sdk_exceptions.SdkInvalidClient


def client(s: str):
    return ClientFactory.create_client(s)

import typing
from dataclasses import dataclass

from ggcore import sdk_exceptions
from ggcore.client import ConfigClient, SecurityClient, GraphGridModuleClient
from ggcore.utils import CONFIG, SECURITY


class GraphGridModuleClientFactory:
    def create_client_instance(self) -> GraphGridModuleClient:
        pass


class ConfigClientFactory(GraphGridModuleClientFactory):
    def create_client_instance(self) -> GraphGridModuleClient:
        return ConfigClient()


class SecurityClientFactory(GraphGridModuleClientFactory):
    def create_client_instance(self) -> GraphGridModuleClient:
        return SecurityClient()


@dataclass
class FactoryData:
    client_name: str
    factory: GraphGridModuleClientFactory


class ClientFactory:
    _FACTORIES_DATA: typing.Dict[str, FactoryData] = {
        CONFIG: FactoryData(CONFIG, ConfigClientFactory()),
        SECURITY: FactoryData(SECURITY, SecurityClientFactory()),
    }

    @classmethod
    def call_module_client_factory(cls, validated_client_name) -> GraphGridModuleClient:
        return cls._FACTORIES_DATA.get(validated_client_name).factory.create_client_instance()

    @classmethod
    def create_client(cls, client_name) -> GraphGridModuleClient:
        if client_name in cls._FACTORIES_DATA:
            return cls.call_module_client_factory(client_name)
        else:
            raise sdk_exceptions.SdkInvalidClient


def client(s: str) -> GraphGridModuleClient:
    return ClientFactory.create_client(s)

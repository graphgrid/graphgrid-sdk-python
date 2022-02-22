import typing
from dataclasses import dataclass

from ggcore import sdk_exceptions
from ggcore.client import ConfigClient, SecurityClient, GraphGridModuleClient, NlpClient
from ggcore.utils import CONFIG, SECURITY, NLP


class GraphGridModuleClientFactory:
    def create_client_instance(self, url_base) -> GraphGridModuleClient:
        pass


class ConfigClientFactory(GraphGridModuleClientFactory):
    def create_client_instance(self, url_base) -> GraphGridModuleClient:
        return ConfigClient(url_base)


class SecurityClientFactory(GraphGridModuleClientFactory):
    def create_client_instance(self, url_base) -> GraphGridModuleClient:
        return SecurityClient(url_base)


class NlpClientFactory(GraphGridModuleClientFactory):
    def create_client_instance(self, url_base) -> GraphGridModuleClient:
        return NlpClient(url_base)


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
    def call_module_client_factory(cls, validated_client_name, url_base) -> GraphGridModuleClient:
        return cls._FACTORIES_DATA.get(validated_client_name).factory.create_client_instance(url_base)

    @classmethod
    def create_client(cls, client_name, url_base) -> GraphGridModuleClient:
        if client_name in cls._FACTORIES_DATA:
            return cls.call_module_client_factory(client_name, url_base)
        else:
            raise sdk_exceptions.SdkInvalidClient


# todo the url_base should really be worked in elsewhere, like into the config store (non-existant atm) or totally disconnected from the client anyways
def client(s: str, url_base: str = "localhost") -> GraphGridModuleClient:
    return ClientFactory.create_client(s, url_base)

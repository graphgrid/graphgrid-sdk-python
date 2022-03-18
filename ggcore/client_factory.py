"""Define classes for sdk client factory (unused)."""

import typing
from dataclasses import dataclass

from ggcore import sdk_exceptions
from ggcore.client import ConfigClient, SecurityClient, NlpClient, ClientBase
from ggcore.utils import CONFIG, SECURITY, NLP


# todo remove this file? could be used in the future, but currently unused

# pylint: disable=too-few-public-methods
class GraphGridModuleClientFactory:
    """Define client factory base class."""

    def create_client_instance(self) -> ClientBase:
        """Create and return a client instance."""


class ConfigClientFactory(GraphGridModuleClientFactory):
    """Define Config client factory."""

    def create_client_instance(self) -> ClientBase:
        return ConfigClient(None)


class SecurityClientFactory(GraphGridModuleClientFactory):
    """Define Security client factory."""

    def create_client_instance(self) -> ClientBase:
        return SecurityClient(None)


class NlpClientFactory(GraphGridModuleClientFactory):
    """Define Nlp client factory."""

    def create_client_instance(self) -> ClientBase:
        return NlpClient(None)


@dataclass
class FactoryData:
    """Define class encapsulating factory information."""
    client_name: str
    factory: GraphGridModuleClientFactory


class ClientFactory:
    """Create clients from client factories."""

    _FACTORIES_DATA: typing.Dict[str, FactoryData] = {
        CONFIG: FactoryData(CONFIG, ConfigClientFactory()),
        SECURITY: FactoryData(SECURITY, SecurityClientFactory()),
        NLP: FactoryData(NLP, NlpClientFactory()),
    }

    @classmethod
    def call_module_client_factory(cls, validated_client_name) -> ClientBase:
        """Get client factory and create a client instance."""
        return cls._FACTORIES_DATA.get(
            validated_client_name).factory.create_client_instance()

    @classmethod
    def create_client(cls, client_name) -> ClientBase:
        """Create client from string."""
        if client_name in cls._FACTORIES_DATA:
            return cls.call_module_client_factory(client_name)
        raise sdk_exceptions.SdkInvalidClient


def client(client_name: str) -> ClientBase:
    """Create client from string (unused)."""
    return ClientFactory.create_client(client_name)

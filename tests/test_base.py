"""Define test base classes used throughout the tests."""
from unittest import TestCase

from graphgrid_sdk.ggcore.config import SdkBootstrapConfig


class TestBase(TestCase):
    """Define base for all SDK tests. Utility test methods and test constants
    go in here.
    """
    TEST_TOKEN: str = "test-token"


class TestBootstrapBase(TestBase):
    """Define base for tests that contains the bootstrap config and test
    credentials.
    """

    _test_bootstrap_config = SdkBootstrapConfig(
        access_key='a3847750f486bd931de26c6e683b1dc4',
        secret_key='81a62cea53883f4a163a96355d47656e',
        url_base='localhost',
        is_docker_context=False)


class TestBootstrapDockerBase(TestBase):
    """Define base for tests that mimic running in a docker context.

    Contains the bootstrap config, test credentials, and sets
    'is_docker_context' to True.
    """
    _test_bootstrap_docker_config = SdkBootstrapConfig(
        access_key='a3847750f486bd931de26c6e683b1dc4',
        secret_key='81a62cea53883f4a163a96355d47656e',
        url_base="localhost",
        is_docker_context=True)

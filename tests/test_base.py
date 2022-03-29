"""Define test base classes used throughout the tests."""
from unittest import TestCase

from ggcore.config import SdkBootstrapConfig, SdkSecurityConfig


class TestBootstrapBase(TestCase):
    """Define base for tests that contains the bootstrap config and test
    credentials.
    """

    TEST_TOKEN: str = "test-token"

    _test_bootstrap_config = SdkBootstrapConfig(
        access_key='a3847750f486bd931de26c6e683b1dc4',
        secret_key='81a62cea53883f4a163a96355d47656e',
        url_base='localhost',
        is_docker_context=False)

    _test_credentials = SdkSecurityConfig(_test_bootstrap_config, TEST_TOKEN)


class TestBootstrapDockerBase(TestCase):
    """Define base for tests that mimic running in a docker context.

    Contains the bootstrap config, test credentials, and sets
    'is_docker_context' to True.
    """

    TEST_TOKEN: str = "test-token"

    _test_bootstrap_docker_config = SdkBootstrapConfig(
        access_key='a3847750f486bd931de26c6e683b1dc4',
        secret_key='81a62cea53883f4a163a96355d47656e',
        url_base="localhost",
        is_docker_context=True)

    _test_credentials = SdkSecurityConfig(_test_bootstrap_docker_config, TEST_TOKEN)

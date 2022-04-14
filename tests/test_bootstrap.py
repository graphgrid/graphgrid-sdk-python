"""Define test classes for SDK bootstrapping."""
import os
from unittest import mock

from graphgrid_sdk.ggsdk.sdk import GraphGridSdk
from tests.test_base import TestBootstrapBase, TestBase


class TestBootstrapAutoConfig(TestBootstrapBase):
    """Define class for testing the boostrap autoconfig."""

    # pylint: disable=broad-except,no-self-use
    @mock.patch.dict(os.environ, {
        "GRAPHGRID_CONFIG_CREDENTIALS_PATH": f"{TestBase.TEST_DIR_LOCATION}/resources",
        "CONFIG_CREDENTIAL_PROPERTIES_FILENAME": "configCredentials.properties"})
    def test_auto_config(self):
        """Define test that automagically sets up GraphGridSdk config."""
        try:
            GraphGridSdk()
        except Exception:
            assert False, \
                "Hit error while setting up SDK using autoconfig bootstrapping."

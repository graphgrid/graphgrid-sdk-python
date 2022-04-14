import os
from unittest import mock

from graphgrid_sdk.ggsdk.sdk import GraphGridSdk
from tests.test_base import TestBootstrapBase


class TestBootstrapConfig(TestBootstrapBase):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    @mock.patch.dict(os.environ, {
        "GRAPHGRID_CONFIG_CREDENTIALS_PATH": f"{__location__}/resources",
        "CONFIG_CREDENTIAL_PROPERTIES_FILENAME": "configCredentials.properties"}
        , clear=True)
    def test_auto_config(self):
        try:
            GraphGridSdk()
        except Exception:
            assert False, \
                f"Hit error while setting up SDK using autoconfig bootstrapping."

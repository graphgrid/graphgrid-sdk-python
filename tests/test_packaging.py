from unittest import TestCase

from ggcore.credentials import Credentials
from ggsdk.session import GraphGridSession


class TestConnections(TestCase):
    _test_credentials = Credentials(access_key='a3847750f486bd931de26c6e683b1dc4',
                                    secret_key='81a62cea53883f4a163a96355d47656e',
                                    token="d04ce18b-24ba-4a49-b80a-cf3730f36908")

    def test_packaging_test(self):
        """

        """
        session = GraphGridSession(url_base="localhost", access_key=self._test_credentials.access_key, secret_access_key=self._test_credentials.secret_key)

        session.setup_security_client()

        print("testing through the packaging setup")

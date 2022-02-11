from unittest import TestCase

from ggcore import utils, factory


class TestFactory(TestCase):

    def test_client(self):
        """
        Tests that the factory instantiates each supported client object.
        """
        for client in utils.SUPPORTED_CLIENTS:
            assert client == factory.client(client).client_name

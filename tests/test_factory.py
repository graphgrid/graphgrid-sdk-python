from unittest import TestCase

from ggcore import client_factory, utils


class TestFactory(TestCase):

    def test_client_objects(self):
        """
        Tests that the factory instantiates all supported client object.
        """
        for client in utils.SUPPORTED_CLIENTS:
            self.assertEqual(client,client_factory.client(client).client_name, f"Supported client '{client}' failed to return its client factory object.")


    def test_invalid_client(self):
        with self.assertRaises(ValueError) as context:
            client_factory.client("invalid")

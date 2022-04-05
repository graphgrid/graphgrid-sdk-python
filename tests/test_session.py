"""Define test classes for session features and TokenFactory."""
from unittest.mock import patch

import responses

import ggcore
from ggcore.api import SecurityApi
from ggcore.client import SecurityClient
from ggcore.session import TokenFactory
from ggcore.utils import RequestAuthType
from tests.test_base import TestBootstrapBase


class TestTokenFactory(TestBootstrapBase):
    """Define test class for grouping TokenFactory feature tests."""

    # pylint: disable=unused-argument
    @responses.activate  # mock responses
    @patch.object(ggcore.security_base.BearerAuth, "get_auth_value",
                  return_value=TestBootstrapBase.TEST_TOKEN)
    def test_token_factory__get_token_if_missing(self, mock_get_auth_value):
        """Test new token retrieved if no current token."""

        security_client = SecurityClient(self._test_bootstrap_config)
        token_factory = TokenFactory(security_client.get_token_builtin)

        json_body = {"access_token": self.TEST_TOKEN,
                     "token_type": RequestAuthType.BEARER.value,
                     "expires_in": 50_000,
                     "createdAt": "2022-04-01T19:48:47.647Z"}

        responses.add(responses.POST,
                      f'http://localhost/1.0/security/'
                      f'{SecurityApi.get_token_api().endpoint()}',
                      json=json_body, status=200)

        if token_factory.is_token_ready():
            assert False, "Token should not be present yet."

        # run token handling
        token_factory.refresh_token()

        if token_factory.is_token_ready():
            return

        assert False, "Token should be present after token_handling call."

    def test_token_factory__expired_token__expiration_logic(self):
        """Test expiration logic functions properly."""

    @responses.activate
    def test_token_factory__expired_token__get_new_token_after_expiry(self):
        """Test new token retrieved after current token expires."""

        expiration_time_for_test_ms = 1_000  # expiration time in ms

        security_client = SecurityClient(self._test_bootstrap_config)
        token_factory = TokenFactory(security_client.get_token_builtin)

        json_body = {"access_token": self.TEST_TOKEN,
                     "token_type": RequestAuthType.BEARER.value,
                     "expires_in": str(expiration_time_for_test_ms),  # cast?
                     "createdAt": "2022-04-01T19:48:47.647Z"}

        responses.add(responses.POST,
                      f'http://localhost/1.0/security/'
                      f'{SecurityApi.get_token_api().endpoint()}',
                      json=json_body, status=200)

        token_factory.refresh_token()

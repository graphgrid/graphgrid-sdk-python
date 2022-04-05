"""Define test classes for session features and TokenFactory."""
import time
from unittest.mock import patch

import responses

import ggcore
from ggcore.api import SecurityApi
from ggcore.client import InternalSecurityClient
from ggcore.session import TokenFactory
from ggcore.utils import RequestAuthType
from tests.test_base import TestBootstrapBase, TestBase


class TestTokenFactory(TestBootstrapBase):
    """Define test class for grouping TokenFactory feature tests."""

    # pylint: disable=unused-argument,protected-access
    @responses.activate  # mock responses
    @patch.object(ggcore.security_base.BearerAuth, "get_auth_value",
                  return_value=TestBootstrapBase.TEST_TOKEN)
    def test_token_factory__get_token_if_missing(self, mock_get_auth_value):
        """Test new token retrieved if no current token."""

        security_client = InternalSecurityClient(self._test_bootstrap_config)
        token_factory = TokenFactory(security_client._get_token_builtin,
                                     security_client._check_token_builtin)

        json_body = {"access_token": TestBase.TEST_TOKEN,
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

    # pylint: disable=protected-access
    @responses.activate
    def test_token_factory__expired_token__get_new_token_after_expiry(self):
        """Test new token retrieved after current token expires."""

        test_expiration_time_ms = 5_000  # expiration time in ms
        test_token_after_expiry = "token-after-expiry"

        security_client = InternalSecurityClient(self._test_bootstrap_config)
        token_factory = TokenFactory(security_client._get_token_builtin,
                                     security_client._check_token_builtin)

        json_body = {"access_token": TestBase.TEST_TOKEN,
                     "token_type": RequestAuthType.BEARER.value,
                     "expires_in": str(test_expiration_time_ms),
                     "createdAt": "2022-04-01T19:48:47.647Z"}

        responses.add(responses.POST,
                      f'http://localhost/1.0/security/'
                      f'{SecurityApi.get_token_api().endpoint()}',
                      json=json_body, status=200)

        # populate token tracker with current mock response
        token_factory.call_get_token()

        # sleep until expiry
        time.sleep(test_expiration_time_ms // 1000)

        # assert token has expired
        assert token_factory.is_token_expired() is True

        # update new token after timeout
        json_body["access_token"] = test_token_after_expiry
        # modify get token response to return new token
        responses.add(responses.POST,
                      f'http://localhost/1.0/security/'
                      f'{SecurityApi.get_token_api().endpoint()}',
                      json=json_body, status=200)

        # refresh token (always requests new token since current
        # token is expired)
        token_factory.refresh_token()

        # assert the new token (now current token) has changed to the new
        # mock response.
        assert token_factory.get_current_token() == test_token_after_expiry

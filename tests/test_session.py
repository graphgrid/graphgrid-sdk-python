"""Define test classes for session features and TokenFactory."""
import time

import responses

from graphgrid_sdk.ggcore.api import SecurityApi
from graphgrid_sdk.ggcore.client import InternalSecurityClient
from graphgrid_sdk.ggcore.session import TokenFactory
from graphgrid_sdk.ggcore.utils import RequestAuthType
from tests.test_base import TestBootstrapBase, TestBase


class TestTokenFactory(TestBootstrapBase):
    """Define test class for grouping TokenFactory feature tests."""

    # pylint: disable=protected-access
    @responses.activate
    def test_token_factory__get_token_if_missing(self):
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

    # pylint: disable=protected-access
    @responses.activate
    def test_token_factory__expired_token(self):
        """Test token expires properly and new token retrieved after
        expiration.
        """

        test_expiration_time_s = 5  # expiration time in seconds
        test_token_after_expiry = "token-after-expiry"

        security_client = InternalSecurityClient(self._test_bootstrap_config)
        token_factory = TokenFactory(security_client._get_token_builtin,
                                     security_client._check_token_builtin)

        json_body = {"access_token": TestBase.TEST_TOKEN,
                     "token_type": RequestAuthType.BEARER.value,
                     "expires_in": str(test_expiration_time_s),
                     "createdAt": "2022-04-01T19:48:47.647Z"}

        responses.add(responses.POST,
                      f'http://localhost/1.0/security/'
                      f'{SecurityApi.get_token_api().endpoint()}',
                      json=json_body, status=200)

        # populate token tracker with current mock response
        token_factory.call_get_token()

        # assert token has not yet expired
        assert token_factory.is_token_expired() is False

        # sleep until expiry
        time.sleep(test_expiration_time_s)

        # assert token has expired
        assert token_factory.is_token_expired() is True

        # update new token after timeout
        json_body["access_token"] = test_token_after_expiry
        # modify mock get token response to use updated json body
        responses.add(responses.POST,
                      f'http://localhost/1.0/security/'
                      f'{SecurityApi.get_token_api().endpoint()}',
                      json=json_body, status=200)

        # refresh token
        token_factory.refresh_token()

        # assert the current token is updated and matches the mock response
        # token value.
        assert token_factory.get_current_token() == test_token_after_expiry

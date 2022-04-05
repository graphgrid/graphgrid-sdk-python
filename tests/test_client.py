"""Define test classes for testing client-level features."""
# pylint: disable=duplicate-code
from unittest.mock import patch

import ggcore.http_base
from ggcore.api import ConfigApi, AbstractApi
from ggcore.client import ConfigClient
from ggcore.sdk_messages import SdkServiceRequest
from ggcore.security_base import SdkAuthHeaderBuilder
from ggcore.session import TokenTracker
from ggcore.utils import HttpMethod, DOCKER_NGINX_PORT
from tests.test_base import TestBootstrapBase, TestBootstrapDockerBase, \
    TestBase


class TestClientBase(TestBootstrapBase):
    """Define test base for client-level tests."""


class TestClientSdkRequestBuilding(TestClientBase):
    """Define test class for grouping client-level sdk request building."""

    # pylint: disable=unused-argument
    @patch.object(ggcore.session.TokenFactory, "_token_tracker",
                  TokenTracker(TestBase.TEST_TOKEN, 10_000))
    def test_client_feature__build_sdk_request__test_api(self):
        """Test that client can properly construct test api sdk request from
        TestApi definition.
        """

        # get TestApi definition
        test_api = ConfigApi.test_api()

        # setup config client
        config_client = ConfigClient(self._test_bootstrap_config)

        # setup expected service request
        expected = SdkServiceRequest()
        expected.http_method = HttpMethod.GET
        expected.api_endpoint = "config/this/is/a/test"
        expected.headers = AbstractApi().headers()
        expected.add_headers(SdkAuthHeaderBuilder.get_bearer_header(
            TestBase.TEST_TOKEN))
        expected.query_params = {}
        expected.body = {}
        expected.url = f'http://localhost/1.0/{expected.api_endpoint}'

        # build actual service request from api definition
        actual = config_client.build_sdk_request(test_api)

        # assert actual request equals expected request
        assert actual == expected

    def test_client_feature__build_sdk_request__save_dataset(self):
        """Test client properly constructs save dataset sdk request from
        SaveDatasetApi definition.
        """

    def test_client_feature__build_sdk_request__get_data(self):
        """Test client properly constructs get data sdk request from
        GetDataApi definition.
        """

    def test_client_feature__build_sdk_request__promote_model(self):
        """Test client properly constructs promote model sdk request from
        PromoteModelApi definition.
        """

    def test_client_feature__build_sdk_request__check_token(self):
        """Test client properly constructs check token sdk request from
        CheckTokenApi definition.
        """


class TestClientResponseHandling(TestClientBase):
    """Define test class for grouping client-level generic response handling."""

    def test_client_feature__call_api_handling__401_response__200_check_token(
            self):
        """Test built-in client ability to handle 401 Unauthorized. This test
        is specifically when 401 Unauthorized leads to a 200 OK from a
        check_token call.

        Expected behavior pushes up the original error response along with a
        message notifying the user the token was invalid even after getting a
        new one.
        """

    def test_client_feature__call_api_handling__401_response__400_check_token(
            self):
        """Test built-in client ability to handle 401 Unauthorized. This test
        specifically covers when 401 Unauthorized leads to a 400 Bad Request
        from a check_token call.

        Test asserts
        (1) token handling grabs a new token after a 401 Unauthorized original
            request and 200 OK check_token.
        (2) The original request is retried with the new token.
        (3) A subsequent request returns the result.
            (subsequent 401s return with error, break into separate test?)
        """


class TestClientDockerContext(TestBootstrapDockerBase):
    """Define test class for grouping client-level docker context features.

    Uses the TestBootstrapDockerBase instead of TestClientBase.
    """

    # pylint: disable=unused-argument
    @patch.object(ggcore.session.TokenFactory, "_token_tracker",
                  TokenTracker(TestBase.TEST_TOKEN, 10_000))
    def test_client_feature__is_docker_context(self):
        """Test that sdk requests built from the test docker base use the
        correct url base for docker.
        """
        # get TestApi definition
        test_api = ConfigApi.test_api()

        # setup config client
        config_client = ConfigClient(self._test_bootstrap_docker_config)

        # setup expected service request
        expected = SdkServiceRequest()
        expected.http_method = HttpMethod.GET
        expected.docker_base = test_api.api_base()
        expected.api_endpoint = "config/this/is/a/test"
        expected.headers = AbstractApi().headers()
        expected.add_headers(
            SdkAuthHeaderBuilder.get_bearer_header(TestBase.TEST_TOKEN))
        expected.query_params = {}
        expected.body = {}
        expected.url = f'http://{test_api.api_base()}:{DOCKER_NGINX_PORT}' \
                       f'/1.0/{expected.api_endpoint}'

        # build actual service request from api definition
        actual = config_client.build_sdk_request(test_api)

        # assert actual request equals expected request
        assert actual == expected

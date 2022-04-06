"""Define test classes for testing client-level features."""
from unittest.mock import patch

from graphgrid_sdk.ggcore.security_base import BearerAuth
from graphgrid_sdk.ggcore.client import SecurityClient
from graphgrid_sdk.ggcore.api import ConfigApi, AbstractApi
from graphgrid_sdk.ggcore.client import ConfigClient
from graphgrid_sdk.ggcore.sdk_messages import SdkServiceRequest
from graphgrid_sdk.ggcore.security_base import SdkAuthHeaderBuilder
from graphgrid_sdk.ggcore.utils import HttpMethod, DOCKER_NGINX_PORT
from tests.test_base import TestBootstrapBase, TestBootstrapDockerBase


class TestClientBase(TestBootstrapBase):
    """Define test base for client-level tests."""


class TestClientSdkRequestBuilding(TestClientBase):
    """Define test class for grouping client-level sdk request building."""

    # pylint: disable=unused-argument
    @patch.object(BearerAuth, "get_auth_value",
                  return_value=TestBootstrapBase.TEST_TOKEN)
    @patch.object(SecurityClient, "is_token_present",
                  return_value="true")
    def test_client_feature__build_sdk_request__test_api(self,
                                                         mock_get_auth_value,
                                                         mock_is_token_present):
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
            self._test_credentials))
        expected.query_params = {}
        expected.body = {}
        expected.api_response_handler = AbstractApi().handler
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


class TestClientGenericResponseHandling(TestClientBase):
    """Define test class for grouping client-level generic response handling."""

    def test_client_feature__generic_response_handling__500(self):
        """Test built-in client ability to handle 500 Internal Server Error."""

    def test_client_feature__generic_response_handling__401(self):
        """Test built-in client ability to handle 401 Unauthorized.

        This test covers:
            (1) token handling grabs a new token after a 401 Unauthorized.
            (2) 401 Unauthorized are retried automatically.
            (3) A subsequent 401 returns a response with an error.
        """


class TestClientDockerContext(TestBootstrapDockerBase):
    """Define test class for grouping client-level docker context features.

    Uses the TestBootstrapDockerBase instead of TestClientBase.
    """

    # pylint: disable=unused-argument
    @patch.object(BearerAuth, "get_auth_value",
                  return_value=TestBootstrapBase.TEST_TOKEN)
    @patch.object(SecurityClient, "is_token_present",
                  return_value="true")
    def test_client_feature__is_docker_context(self, mock_get_auth_value,
                                               mock_is_token_present):
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
        expected.add_headers(SdkAuthHeaderBuilder.get_bearer_header(
            self._test_credentials))
        expected.query_params = {}
        expected.body = {}
        expected.api_response_handler = AbstractApi().handler
        expected.url = f'http://{test_api.api_base()}:{DOCKER_NGINX_PORT}' \
                       f'/1.0/{expected.api_endpoint}'

        # build actual service request from api definition
        actual = config_client.build_sdk_request(test_api)

        # assert actual request equals expected request
        assert actual == expected

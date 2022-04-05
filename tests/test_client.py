"""Define test classes for testing client-level features."""
from unittest.mock import patch

import responses

import ggcore.http_base
from ggcore.api import ConfigApi, AbstractApi, SecurityApi
from ggcore.client import ConfigClient
from ggcore.sdk_exceptions import SdkInvalidOauthCredentialsException, \
    SdkUnauthorizedValidTokenException
from ggcore.sdk_messages import SdkServiceRequest
from ggcore.security_base import SdkAuthHeaderBuilder
from ggcore.session import TokenTracker
from ggcore.utils import HttpMethod, DOCKER_NGINX_PORT, RequestAuthType
from tests.test_base import TestBootstrapBase, TestBootstrapDockerBase, \
    TestBase


class TestClientBase(TestBootstrapBase):
    """Define test base for client-level tests."""


class TestClientSdkRequestBuilding(TestClientBase):
    """Define test class for grouping client-level sdk request building."""

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

    @responses.activate
    def test_client_feature__unauth_response_handling__check_token_200(self):
        """Test client ability to deal with 401 Unauthorized response.

        This test asserts an error is raised when the sdk response is
        401 Unauthorized and that leads to a 200 OK from check_token.
        """

        json_body = {"access_token": TestBase.TEST_TOKEN,
                     "token_type": RequestAuthType.BEARER.value,
                     "expires_in": 10_000,
                     "createdAt": "2022-04-01T19:48:47.647Z"}

        # mock get token response 200
        responses.add(responses.POST,
                      f'http://localhost/1.0/security/'
                      f'{SecurityApi.get_token_api().endpoint()}',
                      json=json_body, status=200)

        # mock test_api response 401
        responses.add(responses.GET,
                      f'http://localhost/1.0/config/'
                      f'{ConfigApi.test_api().endpoint()}',
                      json={}, status=401)

        # mock check token response 200
        responses.add(responses.POST,
                      f'http://localhost/1.0/security/'
                      f'{SecurityApi.check_token_api().endpoint()}',
                      json={}, status=200)

        # setup config client
        config_client = ConfigClient(self._test_bootstrap_config)

        self.assertRaises(SdkUnauthorizedValidTokenException,
                          config_client.test_api, "test-msg")

    @responses.activate
    def test_client_feature__unauth_response_handling__check_token_400(self):
        """Test client ability to deal with 401 Unauthorized response.

        This test covers when 401 Unauthorized leads to a 400 Bad Request
        from a check_token call. It asserts a new token is retrieved and the
        original request is retried.
        """

    @responses.activate
    def test_client_feature__unauth_response_handling__get_token_401(self):
        """Test exception thrown when token response is 401 Unauthorized."""
        responses.add(responses.POST,
                      f'http://localhost/1.0/security/'
                      f'{SecurityApi.get_token_api().endpoint()}',
                      json={}, status=401)

        # setup config client
        config_client = ConfigClient(self._test_bootstrap_config)

        self.assertRaises(SdkInvalidOauthCredentialsException,
                          config_client.test_api, "test-msg")


class TestClientDockerContext(TestBootstrapDockerBase):
    """Define test class for grouping client-level docker context features.

    Uses the TestBootstrapDockerBase instead of TestClientBase.
    """

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

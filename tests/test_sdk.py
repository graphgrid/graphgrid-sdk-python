"""Define test classes for testing user-facing sdk calls."""
import json
from unittest.mock import patch

import responses

import ggcore
import ggsdk.sdk
from ggcore.api import ConfigApi
from ggcore.sdk_messages import TestApiResponse, SdkResponseHelper
from tests.test_base import TestBootstrapBase


class TestSdkBase(TestBootstrapBase):
    """Define test base specifically for high-level sdk calls."""


class TestSdkTestApi(TestSdkBase):
    """Define test class for TestApi sdk calls."""

    # pylint: disable=unused-argument
    @responses.activate  # mock responses
    @patch.object(ggcore.security_base.BearerAuth, "get_auth_value",
                  return_value=TestBootstrapBase.TEST_TOKEN)
    @patch.object(ggcore.session.TokenFactory, "is_token_ready",
                  return_value="true")
    def test_sdk_call__test_api__200(self, mock_get_auth_value,
                                     mock_is_token_present):
        """Test sdk TestApi call when response is 200 OK.

        Test that the GraphGridSdk.test_api() call sets up correct sdk
        request and can handle responses properly.

        Works by mocking http response and ensure we get back the expected
        TestApiResponse.
        """

        # setup expected message and json body for test
        expected_message = "pass me back and forth"
        json_body = {"content": expected_message}

        # setup sdk
        sdk = ggsdk.sdk.GraphGridSdk(self._test_bootstrap_config.access_key,
                                     self._test_bootstrap_config.secret_key,
                                     self._test_bootstrap_config.url_base)

        # setup responses mock
        responses.add(responses.GET,
                      f'http://localhost/1.0/config/'
                      f'{ConfigApi.test_api().endpoint()}',
                      json=json_body, status=200)

        # setup expected TestApiResponse obj
        expected_response = TestApiResponse(
            SdkResponseHelper(200, "OK", json.dumps(json_body), None))

        # call sdk method for test api
        actual_response: TestApiResponse = sdk.test_api(expected_message)

        # assert that the TestApiResponse returned is the same as the
        # expected response
        assert actual_response == expected_response


class TestSdkSaveDataset(TestSdkBase):
    """Define test class for SaveDatasetApi sdk calls."""

    def test_sdk_call__save_dataset__200(self):
        """Test sdk SaveDataset call when response is 200 OK."""

    def test_sdk_call__save_dataset__409(self):
        """Test sdk SaveDatasetApi call when response is 409 Conflict."""


class TestSdkGetData(TestSdkBase):
    """Define test class for GetDataApi sdk calls."""

    def test_sdk_call__get_data__200(self):
        """Test sdk GetDataApi call when response is 200 OK."""


class TestSdkPromoteModel(TestSdkBase):
    """Define test class for PromoteModelApi sdk calls."""

    def test_sdk_call__promote_model__200(self):
        """Test sdk PromoteModelApi call when response is 200 OK."""

"""Define test classes for testing user-facing sdk calls."""
import json
from unittest.mock import patch

import responses

import ggcore
import ggsdk.sdk
from ggcore.api import ConfigApi, NlpApi
from ggcore.sdk_messages import TestApiResponse, SdkServiceResponse, \
    GetJobStatusResponse, GetJobResultsResponse, JobTrainResponse
from tests.test_base import TestBootstrapBase


class TestSdkBase(TestBootstrapBase):
    """Define test base specifically for high-level sdk calls."""


class TestSdkTestApi(TestSdkBase):
    """Define test class for TestApi sdk calls."""

    # pylint: disable=unused-argument
    @responses.activate  # mock responses
    @patch.object(ggcore.security_base.BearerAuth, "get_auth_value",
                  return_value=TestBootstrapBase.TEST_TOKEN)
    @patch.object(ggcore.client.SecurityClient, "is_token_present",
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
            SdkServiceResponse(200, "OK", json.dumps(json_body), None))

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


class TestSdkGetJobStatus(TestSdkBase):
    """Define test class for GetJobStatusApi sdk calls."""

    # pylint: disable=unused-argument
    @responses.activate  # mock responses
    @patch.object(ggcore.security_base.BearerAuth, "get_auth_value",
                  return_value=TestBootstrapBase.TEST_TOKEN)
    @patch.object(ggcore.client.SecurityClient, "is_token_present",
                  return_value="true")
    def test_sdk_call__get_job_status__200(self, mock_get_auth_value,
                                           mock_is_token_present):
        """Test sdk GetJobStatusApi call when response is 200 OK."""
        dag_id = "any_dag"
        start_date = "2022-03-28T16:02:45.526226+00:00"
        state = "running"
        dag_run_id = f"manual__{start_date}"
        expected_response_dict = {
            "status_code": 200,
            "status_text": "OK",
            "dag_run_id": dag_run_id,
            "dag_id": dag_id,
            "start_date": start_date,
            "state": state,
            "response": None,
            "exception": None
        }

        sdk = ggsdk.sdk.GraphGridSdk(self._test_bootstrap_config.access_key,
                                     self._test_bootstrap_config.secret_key,
                                     self._test_bootstrap_config.url_base)
        responses.add(method=responses.GET,
                      url=f'http://localhost/1.0/nlp/'
                          f'{NlpApi.get_job_status_api(dag_id=dag_id, dag_run_id=dag_run_id).endpoint()}',
                      json=expected_response_dict, status=200)

        expected_response = GetJobStatusResponse(**expected_response_dict)
        actual_response: GetJobStatusResponse = sdk.get_job_status(
            dag_id=dag_id, dag_run_id=dag_run_id)

        assert actual_response == expected_response


class TestSdkGetJobResults(TestSdkBase):
    """Define test class for GetJobResultsApi sdk calls."""

    # pylint: disable=unused-argument
    @responses.activate  # mock responses
    @patch.object(ggcore.security_base.BearerAuth, "get_auth_value",
                  return_value=TestBootstrapBase.TEST_TOKEN)
    @patch.object(ggcore.client.SecurityClient, "is_token_present",
                  return_value="true")
    def test_sdk_call__get_job_results__200(self, mock_get_auth_value,
                                            mock_is_token_present):
        """Test sdk GetJobResultsApi call when response is 200 OK."""
        dag_id = "any_dag"
        start_date = "2022-03-28T16:02:45.526226+00:00"
        state = "success"
        dag_run_id = f"manual__{start_date}"
        expected_response_dict = {
            "status_code": 200,
            "status_text": "OK",
            "dag_run_id": dag_run_id,
            "dag_id": dag_id,
            "start_date": start_date,
            "state": state,
            "response": None,
            "exception": None
        }

        sdk = ggsdk.sdk.GraphGridSdk(self._test_bootstrap_config.access_key,
                                     self._test_bootstrap_config.secret_key,
                                     self._test_bootstrap_config.url_base)
        responses.add(method=responses.GET,
                      url=f'http://localhost/1.0/nlp/'
                          f'{NlpApi.get_job_results_api(dag_id=dag_id, dag_run_id=dag_run_id).endpoint()}',
                      json=expected_response_dict, status=200)

        expected_response = GetJobResultsResponse(**expected_response_dict)
        actual_response: GetJobResultsResponse = sdk.get_job_results(
            dag_id=dag_id, dag_run_id=dag_run_id)

        assert actual_response == expected_response


class TestSdkJobTrain(TestSdkBase):
    """Define test class for JobTrainApi sdk calls."""

    # pylint: disable=unused-argument
    @responses.activate  # mock responses
    @patch.object(ggcore.security_base.BearerAuth, "get_auth_value",
                  return_value=TestBootstrapBase.TEST_TOKEN)
    @patch.object(ggcore.client.SecurityClient, "is_token_present",
                  return_value="true")
    def test_sdk_call__job_train__200(self, mock_get_auth_value,
                                      mock_is_token_present):
        """Test sdk GetJobResultsApi call when response is 200 OK."""
        dag_id = "any_dag"
        start_date = "2022-03-28T16:02:45.526226+00:00"
        logical_date = "2022-03-28T16:02:45.526226+00:00"
        state = "queued"
        dag_run_id = f"manual__{start_date}"
        expected_response_dict = {
            "status_code": 200,
            "status_text": "OK",
            "dag_run_id": dag_run_id,
            "logical_date": logical_date,
            "state": state,
            "response": None,
            "exception": None
        }
        request_body = {"model": "some-model",
                        "datasets": {"some-dataset": {"train": "path/to/dataset", "eval": "path/to/dataset"},
                                     "another_dataset": {"train": "path/to/dataset", "eval": "path/to/dataset"}},
                        "no_cache": False,
                        "GPU": False}

        sdk = ggsdk.sdk.GraphGridSdk(self._test_bootstrap_config.access_key,
                                     self._test_bootstrap_config.secret_key,
                                     self._test_bootstrap_config.url_base)
        responses.add(method=responses.POST,
                      url=f'http://localhost/1.0/nlp/'
                          f'{NlpApi.job_train_api(request_body=request_body, dag_id=dag_id).endpoint()}',
                      json=expected_response_dict, status=200)

        expected_response = JobTrainResponse(**expected_response_dict)
        actual_response: JobTrainResponse = sdk.job_train(
            request_body=request_body, dag_id=dag_id)

        assert actual_response == expected_response

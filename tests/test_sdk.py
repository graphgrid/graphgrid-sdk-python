"""Define test classes for testing user-facing sdk calls."""
import json
from unittest import mock
from unittest.mock import patch

import requests
import responses

from graphgrid_sdk import ggcore
from graphgrid_sdk.ggcore.api import ConfigApi, NlpApi
from graphgrid_sdk.ggcore.sdk_messages import TestApiResponse, \
    GenericResponse, SaveDatasetResponse, PromoteModelResponse, \
    GetDataResponse, DagRunResponse, NMTTrainResponse, NMTStatusResponse
from graphgrid_sdk.ggcore.session import TokenTracker, TokenFactory
from graphgrid_sdk.ggcore.training_request_body import TrainRequestBody
from graphgrid_sdk.ggsdk import sdk
from graphgrid_sdk.ggsdk.sdk import GraphGridSdk
from tests.test_base import TestBootstrapBase, TestBase


class TestSdkBase(TestBootstrapBase):
    """Define test base specifically for high-level sdk calls."""


class TestSdkTestApi(TestSdkBase):
    """Define test class for TestApi sdk calls."""

    @responses.activate  # mock responses
    @patch.object(TokenFactory, "_token_tracker",
                  TokenTracker(TestBase.TEST_TOKEN, 10_000))
    def test_sdk_call__test_api__200(self):
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
        gg_sdk = sdk.GraphGridSdk(self._test_bootstrap_config)

        # setup responses mock
        responses.add(responses.GET,
                      f'http://localhost/1.0/config/'
                      f'{ConfigApi.test_api().endpoint()}',
                      json=json_body, status=200)

        # setup expected TestApiResponse obj
        expected_response = TestApiResponse(
            GenericResponse(200, "OK", json.dumps(json_body), None))

        # call sdk method for test api
        actual_response: TestApiResponse = gg_sdk.test_api(expected_message)

        # assert that the TestApiResponse returned is the same as the
        # expected response
        assert actual_response == expected_response


class TestSdkSaveDataset(TestSdkBase):
    """Define test class for SaveDatasetApi sdk calls."""

    @responses.activate  # mock responses
    @patch.object(TokenFactory, "_token_tracker",
                  TokenTracker(TestBase.TEST_TOKEN, 10_000))
    def test_sdk_call__save_dataset__200(self):
        """Test sdk SaveDataset call when response is 200 OK."""

        generator = mock.MagicMock()
        dataset_id = "any_dataset"
        overwrite = False
        expected_response_dict = {
            "datasetId": dataset_id,
            "path": "any/save/location"
        }

        # setup sdk
        gg_sdk = sdk.GraphGridSdk(self._test_bootstrap_config)
        responses.add(method=responses.POST,
                      url=f'http://localhost/1.0/nlp/'
                          f'{NlpApi.save_dataset_api(generator=generator, dataset_id=dataset_id, overwrite=overwrite).endpoint()}',
                      json=expected_response_dict, status=200)

        expected_response = SaveDatasetResponse(GenericResponse(200, "OK", json.dumps(expected_response_dict), None))
        actual_response: SaveDatasetResponse = gg_sdk.save_dataset(data_generator=generator, dataset_id=dataset_id,
                                                                   overwrite=overwrite)

        assert actual_response == expected_response

    @responses.activate  # mock responses
    @patch.object(TokenFactory, "_token_tracker",
                  TokenTracker(TestBase.TEST_TOKEN, 10_000))
    def test_sdk_call__save_dataset__409(self):
        """Test sdk SaveDatasetApi call when response is 409 Conflict."""

        generator = mock.MagicMock()
        dataset_id = "existing_dataset_name"
        overwrite = False

        endpoint = NlpApi.save_dataset_api(generator=generator, dataset_id=dataset_id, overwrite=overwrite).endpoint()
        exception = requests.HTTPError(409, f'Client Error: Conflict for url: http://localhost/1.0/nlp/{endpoint}')

        # setup sdk
        gg_sdk = sdk.GraphGridSdk(self._test_bootstrap_config)
        responses.add(method=responses.POST,
                      url=f'http://localhost/1.0/nlp/{endpoint}',
                      body=exception, status=409)

        with self.assertRaises(requests.HTTPError) as e:
            gg_sdk.save_dataset(data_generator=generator, dataset_id=dataset_id, overwrite=overwrite)

        self.assertEqual(exception, e.exception)


class TestSdkGetData(TestSdkBase):
    """Define test class for GetDataApi sdk calls."""

    @responses.activate  # mock responses
    @patch.object(TokenFactory, "_token_tracker",
                  TokenTracker(TestBase.TEST_TOKEN, 10_000))
    def test_sdk_call__get_data__200(self):
        """Test sdk GetDataApi call when response is 200 OK."""

        module = "nlp"
        profiles = ["test"]
        revision = "2.0"
        expected_response_dict = {
            "name": "returned_name",
            "profiles": profiles,
            "label": "returned_label",
            "propertySources": {},
            "version": "returned_version",
            "state": "returned_state"
        }

        # setup sdk
        gg_sdk = sdk.GraphGridSdk(self._test_bootstrap_config)
        responses.add(method=responses.GET,
                      url=f'http://localhost/1.0/config/'
                          f'{ConfigApi.get_data_api(module=module, profiles=profiles, revision=revision).endpoint()}',
                      json=expected_response_dict, status=200)

        expected_response = GetDataResponse(GenericResponse(200, "OK", json.dumps(expected_response_dict), None))
        actual_response: GetDataResponse = gg_sdk.get_data(module=module, profiles=profiles, revision=revision)

        assert actual_response == expected_response


class TestSdkPromoteModel(TestSdkBase):
    """Define test class for PromoteModelApi sdk calls."""

    @responses.activate  # mock responses
    @patch.object(TokenFactory, "_token_tracker",
                  TokenTracker(TestBase.TEST_TOKEN, 10_000))
    def test_sdk_call__promote_model__200(self):
        """Test sdk PromoteModelApi call when response is 200 OK."""
        model_name = "any_model"
        nlp_task = "some_task"
        environment = "default"
        expected_response_dict = {
            "modelName": model_name,
            "task": nlp_task,
            "paramKey": "param_key"
        }

        # setup sdk
        gg_sdk = sdk.GraphGridSdk(self._test_bootstrap_config)
        responses.add(method=responses.POST,
                      url=f'http://localhost/1.0/nlp/'
                          f'{NlpApi.promote_model_api(model_name=model_name, nlp_task=nlp_task, environment=environment).endpoint()}',
                      json=expected_response_dict, status=200)

        expected_response = PromoteModelResponse(GenericResponse(200, "OK", json.dumps(expected_response_dict), None))
        actual_response: PromoteModelResponse = gg_sdk.promote_model(model_name=model_name, nlp_task=nlp_task,
                                                                     environment=environment)


class TestSdkGetJobStatus(TestSdkBase):
    """Define test class for GetDagRunStatusApi sdk calls."""

    # pylint: disable=unused-argument,line-too-long
    @responses.activate  # mock responses
    @patch.object(ggcore.session.TokenFactory, "_token_tracker",
                  TokenTracker(TestBase.TEST_TOKEN, 10_000))
    def test_sdk_call__job_status__200(self):
        """Test sdk GetDagRunStatusApi call when response is 200 OK."""
        dag_id = "any_dag"
        start_date = "2022-03-28T16:02:45.526226+00:00"
        state = "running"
        dag_run_id = f"manual__{start_date}"
        expected_response_dict = {
            "status_code": 200,
            "status_text": "OK",
            "dagRunId": dag_run_id,
            "dagId": dag_id,
            "startDate": start_date,
            "state": state,
            "response": None,
            "exception": None
        }

        gg_sdk = GraphGridSdk(self._test_bootstrap_config)
        responses.add(method=responses.GET,
                      url=f'http://localhost/1.0/nlp/'
                          f'{NlpApi.get_dag_run_status_api(dag_id=dag_id, dag_run_id=dag_run_id).endpoint()}',
                      json=expected_response_dict, status=200)

        expected_response = DagRunResponse(
            GenericResponse(200, "OK", json.dumps(expected_response_dict),
                            None))
        actual_response: DagRunResponse = gg_sdk.job_status(
            dag_id=dag_id, dag_run_id=dag_run_id)

        assert actual_response == expected_response


class TestSdkGetJobResults(TestSdkBase):
    """Define test class for GetJobResultsApi sdk calls."""

    # pylint: disable=unused-argument,line-too-long
    @responses.activate  # mock responses
    @patch.object(ggcore.session.TokenFactory, "_token_tracker",
                  TokenTracker(TestBase.TEST_TOKEN, 10_000))
    # todo get_nmt_status
    def test_sdk_call__nmt_status__200(self):
        """Test sdk GetJobResultsApi call when response is 200 OK."""
        dag_id = "any_dag"
        start_date = "2022-03-28T16:02:45.526226+00:00"
        state = "success"
        dag_run_id = f"manual__{start_date}"
        model_name = "20220328T160245-nerModel"
        expected_response_dict = {
            "status_code": 200,
            "status_text": "OK",
            "dagRunId": dag_run_id,
            "dagId": dag_id,
            "startDate": start_date,
            "state": state,
            "savedModelName": model_name,
            "savedModelFilename": f"{model_name}.tar.gz",
            "savedModelUrl": f"http://minio:9000/com-graphgrid-nlp/2.0.0/{model_name}/{model_name}.tar.gz",
            "response": None,
            "exception": None,
            "trainingAccuracy": .999,
            "trainingLoss": .001,
            "evalAccuracy": .845,
            "evalLoss": .125,
            "properties": {"languages": ["en"]},
        }

        gg_sdk = GraphGridSdk(self._test_bootstrap_config)
        responses.add(method=responses.GET,
                      url=f'http://localhost/1.0/nlp/'
                          f'{NlpApi.nmt_status_api(dag_run_id=dag_run_id).endpoint()}',
                      json=expected_response_dict, status=200)

        expected_response = NMTStatusResponse(
            GenericResponse(200, "OK", json.dumps(expected_response_dict),
                            None))
        actual_response: NMTStatusResponse = gg_sdk.nmt_status(dag_run_id=dag_run_id)

        assert actual_response == expected_response


class TestSdkJobTrain(TestSdkBase):
    """Define test class for TriggerDagApi sdk calls."""

    # pylint: disable=unused-argument,line-too-long
    @responses.activate  # mock responses
    @patch.object(ggcore.session.TokenFactory, "_token_tracker",
                  TokenTracker(TestBase.TEST_TOKEN, 10_000))
    def test_sdk_call__nmt_train__200(self):
        """Test sdk GetJobResultsApi call when response is 200 OK."""
        dag_id = "any_dag"
        start_date = "2022-03-28T16:02:45.526226+00:00"
        logical_date = "2022-03-28T16:02:45.526226+00:00"
        state = "queued"
        dag_run_id = f"manual__{start_date}"
        expected_response_dict = {
            "status_code": 200,
            "status_text": "OK",
            "dagRunId": dag_run_id,
            "logicalDate": logical_date,
            "state": state,
            "response": None,
            "exception": None
        }
        request_body = TrainRequestBody(model="some-model",
                                   datasets={
                                       "some-dataset": {"train": "path/to/dataset",
                                                        "eval": "path/to/dataset"},
                                       "another_dataset": {"train": "path/to/dataset",
                                                           "eval": "path/to/dataset"}},
                                   no_cache=False,
                                   GPU=False)

        gg_sdk = GraphGridSdk(self._test_bootstrap_config)
        responses.add(method=responses.POST,
                      url=f'http://localhost/1.0/nlp/'
                          f'{NlpApi.nmt_train_api(request_body=request_body).endpoint()}',
                      json=expected_response_dict, status=200)

        expected_response = NMTTrainResponse(
            GenericResponse(200, "OK", json.dumps(expected_response_dict),
                            None))
        actual_response: NMTTrainResponse = gg_sdk.nmt_train(
            request_body=request_body)

        assert actual_response == expected_response

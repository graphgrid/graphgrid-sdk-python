"""Define user-facing GraphGrid SDK."""
import typing

from graphgrid_sdk.ggcore.config import SdkBootstrapConfig
from graphgrid_sdk.ggcore.core import SdkCore
from graphgrid_sdk.ggcore.sdk_messages import TestApiResponse, \
    SaveDatasetResponse, GetDataResponse, PromoteModelResponse, \
    GetJobResultsResponse, GetJobStatusResponse, JobTrainResponse
from graphgrid_sdk.ggsdk.bootstrap import bootstrap_config_from_file


class GraphGridSdk:
    """Initialize the SDK Core for SDK calls. Expose those SDK calls as
    user-callable methods.
    """
    _core: SdkCore
    _config: SdkBootstrapConfig

    def __init__(self, bootstrap_config: SdkBootstrapConfig = None):
        if bootstrap_config is None:
            bootstrap_config: SdkBootstrapConfig = bootstrap_config_from_file()

        self._config = bootstrap_config
        self._core = SdkCore(self._config)

    def test_api(self,
                 message: str = None) -> TestApiResponse:
        """Call test api.

        :param message:  The test message that is both send and received
        """
        return self._core.test_api(message)

    def save_dataset(self,
                     data_generator: typing.Generator,
                     dataset_id: str = None,
                     overwrite=False) -> SaveDatasetResponse:
        """Call save dataset api.

        :param data_generator:  The generator providing dataset lines
        :param dataset_id:  Name/id for the dataset (default=None)
        :param overwrite:   Whether to overwrite the dataset if it already
            exists (default=False)
        """
        return self._core.save_dataset(data_generator, dataset_id, overwrite)

    def promote_model(self, model_name: str, nlp_task: str,
                      environment: str = "default") -> PromoteModelResponse:
        """Call promote model api.

        :param model_name: Name of the model to promote within cloud storage
        :param nlp_task: The associated NLP task for the given model
        :param environment: The config environment of the param to
            persist (default=default)
        """
        return self._core.promote_model(model_name, nlp_task, environment)

    def get_data(self, module: str,
                 profiles: typing.Union[str, typing.List[str]],
                 revision: str) -> GetDataResponse:
        """Call get data api.

        :param module: Name of the module for the spring param path, e.g., nlp
        :param profiles: List or string for the module's profile, e.g., test
        :param revision: The revision for the associated param path, e.g., 2.0
        """
        return self._core.get_data(module, profiles, revision)

    def get_job_results(self, dag_id: str,
                        dag_run_id: str) -> GetJobResultsResponse:
        """Call get job results api

        :param dag_id: The name or id of the dag
        :param dag_run_id: The unique id for the finished DAG run.
        """
        return self._core.get_job_results(dag_id, dag_run_id)

    def get_job_status(self, dag_id: str,
                       dag_run_id: str) -> GetJobStatusResponse:
        """Call get job status api

        :param dag_id: The name or id of the dag
        :param dag_run_id: The unique id for the DAG run.
        """
        return self._core.get_job_status(dag_id, dag_run_id)

    def job_train(self, request_body: dict, dag_id: str) -> JobTrainResponse:
        """Call job train api

        :param request_body: Config values to be used in DAG run.
        :param dag_id: The name or id of the dag.
        """
        return self._core.job_train(request_body, dag_id)

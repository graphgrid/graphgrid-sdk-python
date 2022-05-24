"""Define user-facing GraphGrid SDK."""
import typing

from graphgrid_sdk.ggcore.config import SdkBootstrapConfig
from graphgrid_sdk.ggcore.core import SdkCore
from graphgrid_sdk.ggcore.nmt_train_pipeline import NmtTrainPipeline
from graphgrid_sdk.ggcore.sdk_messages import TestApiResponse, \
    SaveDatasetResponse, GetDataResponse, PromoteModelResponse, \
    DagRunResponse, NMTTrainResponse, NMTStatusResponse, TrainRequestBody, \
    NMTTrainPipelineResponse
from graphgrid_sdk.ggcore.utils import NlpModel
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
                     filename: str = None) -> SaveDatasetResponse:
        """Call save dataset api.

        :param data_generator:  The generator providing dataset lines
        :param filename:  filename for the dataset (default=None)
            exists (default=False)
        """
        return self._core.save_dataset(data_generator, filename)

    def promote_model(self, model_name: str,
                      environment: str = "default") -> PromoteModelResponse:
        """Call promote model api.

        :param model_name: Name of the model to promote within cloud storage
        :param environment: The config environment of the param to
            persist (default=default)
        """
        return self._core.promote_model(model_name, environment)

    def get_data(self, module: str,
                 profiles: typing.Union[str, typing.List[str]],
                 revision: str) -> GetDataResponse:
        """Call get data api.

        :param module: Name of the module for the spring param path, e.g., nlp
        :param profiles: List or string for the module's profile, e.g., test
        :param revision: The revision for the associated param path, e.g., 2.0
        """
        return self._core.get_data(module, profiles, revision)

    def job_status(self, dag_id: str,
                   dag_run_id: str) -> DagRunResponse:
        """Call for the job (DAGRun) status

        :param dag_id: The name or id of the DAG
        :param dag_run_id: The unique id for the DAG run.
        """
        return self._core.get_dag_status(dag_id, dag_run_id)

    def job_run(self, dag_id: str, request_body: dict) -> DagRunResponse:
        """Call DAG to start the DAGRun

        :param dag_id: The name or id of the DAG
        :param request_body: Config values to be used in DAG run.
        """
        return self._core.trigger_dag(dag_id, request_body)

    def nmt_status(self, dag_run_id: str) -> NMTStatusResponse:
        """Call to get NMT DAG run status/results

        :param dag_run_id: The unique id for the DAG run.
        """
        return self._core.get_nmt_status(dag_run_id)

    def nmt_train(self, request_body: TrainRequestBody) -> NMTTrainResponse:
        """Call to start trigger NMT DAG

        :param request_body: Training config.
        """
        return self._core.nmt_train(request_body)

    def get_active_model(self, nlp_task: str):
        """Call get active model api.

        :param nlp_task: The associated NLP task for the desired model
        """
        return self._core.get_active_model(nlp_task)

    def nmt_train_pipeline(self, models_to_train: typing.List[NlpModel],
                           datasetId: str,
                           no_cache: typing.Optional[bool],
                           gpu: typing.Optional[bool],
                           autopromote: bool,
                           success_handler: typing.Optional[callable],
                           failed_handler: typing.Optional[
                               callable]) -> NMTTrainPipelineResponse:
        """Call to start training pipeline: kicks off and monitors training for specified tasks, then promotes

        :param models_to_train: List of models to train.
        :param datasetId: Dataset to train on.
        :param no_cache: Flag to prevent caching (defaults to False)
        :param gpu: Flag to enable GPU usage (defaults to False)
        :param autopromote: Flag to enable automatic promotion on successfully trained models.
        :param success_handler: Optional callable to run on a successful training.
        :param failed_handler: Optional callable to run on a failed training.
        """
        pipeline = NmtTrainPipeline(self._config)
        return pipeline.nmt_train_pipeline(models_to_train, datasetId, no_cache,
                                           gpu, autopromote, success_handler,
                                           failed_handler)

"""Define the SDK core entrypoint for sdk calls."""
import typing

from graphgrid_sdk.ggcore.client import ConfigClient, NlpClient
from graphgrid_sdk.ggcore.config import SdkBootstrapConfig
from graphgrid_sdk.ggcore.sdk_messages import SaveDatasetResponse, \
    PromoteModelResponse, GetDataResponse, \
    DagRunResponse, NMTTrainResponse, NMTStatusResponse, TrainRequestBody


class SdkCore:
    """Define core sdk class to hold sdk configuration plus all clients used
    for the sdk. Execute the calls coming from GraphGridSdk.
    """
    _configuration: SdkBootstrapConfig

    _config_client: ConfigClient
    _nlp_client: NlpClient

    def __init__(self, bootstrap_config: SdkBootstrapConfig):
        self._configuration = bootstrap_config

        self._setup_clients()

    def _setup_clients(self):
        """Setup low-level clients."""
        self._config_client = ConfigClient(self._configuration)
        self._nlp_client = NlpClient(self._configuration)

    # Other SDK methods
    def test_api(self, test_message=None):
        """Execute test call. Test purposes only."""
        return self._config_client.test_api(test_message)

    def save_dataset(self, generator: typing.Generator, dataset_id: str,
                     overwrite: bool) -> SaveDatasetResponse:
        """Execute save dataset call."""
        return self._nlp_client.save_dataset(generator=generator,
                                             dataset_id=dataset_id,
                                             overwrite=overwrite)

    def promote_model(self, model_name: str,
                      environment: str) -> PromoteModelResponse:
        """Execute promote model call."""
        return self._nlp_client.promote_model(model_name=model_name,
                                              environment=environment)

    def get_data(self, module: str,
                 profiles: typing.Union[str, typing.List[str]],
                 revision: str) -> GetDataResponse:
        """Execute get data call."""
        return self._config_client.get_data(module, profiles, revision)

    # Generic DAG SDK methods
    def get_dag_status(self, dag_id: str,
                       dag_run_id: str) -> DagRunResponse:
        """Execute get job status call."""
        return self._nlp_client.get_dag_run_status(dag_id, dag_run_id)

    def trigger_dag(self, dag_id: str, request_body: dict) -> DagRunResponse:
        """Execute get job train call."""
        return self._nlp_client.trigger_dag(dag_id, request_body)

    # NMT DAG SDK methods
    def get_nmt_status(self, dag_run_id: str) -> NMTStatusResponse:
        """Execute nmt status call."""
        return self._nlp_client.get_nmt_status(dag_run_id)

    def nmt_train(self, request_body: TrainRequestBody) -> NMTTrainResponse:
        """Execute nmt train call."""
        return self._nlp_client.trigger_nmt(request_body)

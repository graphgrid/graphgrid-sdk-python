"""Define the SDK core entrypoint for sdk calls."""
import typing

from ggcore.client import ConfigClient, NlpClient
from ggcore.config import SdkBootstrapConfig


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

    # test purposes only
    def test_api(self, test_message=None):
        """Execute test call."""
        return self._config_client.test_api(test_message)

    def save_dataset(self, generator: typing.Generator, dataset_id: str,
                     overwrite: bool):
        """Execute save dataset call."""
        return self._nlp_client.save_dataset(generator=generator,
                                             dataset_id=dataset_id,
                                             overwrite=overwrite)

    def promote_model(self, model_name: str, nlp_task: str, environment: str):
        """Execute promote model call."""
        return self._nlp_client.promote_model(model_name=model_name,
                                              nlp_task=nlp_task,
                                              environment=environment)

    def get_data(self, module: str,
                 profiles: typing.Union[str, typing.List[str]],
                 revision: str):
        """Execute get data call."""
        return self._config_client.get_data(module, profiles, revision)

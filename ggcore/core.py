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

    def _setup_clients(self, ):
        """Setup low-level clients."""
        self._config_client = ConfigClient(self._configuration)
        self._nlp_client = NlpClient(self._configuration)

    # test purposes only
    def test_api(self):
        """Execute test call."""
        return self._config_client.test_api()

    def save_dataset(self, generator: typing.Generator, dataset_id: str,
                     overwrite: bool):
        """Execute save dataset call."""
        return self._nlp_client.save_dataset(generator=generator,
                                             dataset_id=dataset_id,
                                             overwrite=overwrite)

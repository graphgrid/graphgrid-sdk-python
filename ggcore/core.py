import typing

from ggcore.client import ConfigClient, NlpClient
from ggcore.config import SdkBootstrapConfig


class SdkCore:
    _configuration: SdkBootstrapConfig

    _config_client: ConfigClient
    _nlp_client: NlpClient

    def __init__(self, bootstrap_config: SdkBootstrapConfig):
        self._configuration = bootstrap_config

        self._setup_clients()

    def _setup_clients(self, ):
        # Setup low-level clients
        self._config_client = ConfigClient(self._configuration)
        self._nlp_client = NlpClient(self._configuration)

    # test purposes only
    def test_api(self):
        return self._config_client.test_api()

    def save_dataset(self, dataset_id: str, generator: typing.Generator, ):
        return self._nlp_client.save_dataset(dataset_id=dataset_id, generator=generator)


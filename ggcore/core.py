import typing

from ggcore.client import ConfigClient, NlpClient
from ggcore.config import SecurityConfig


class SdkCore:
    _configuration: SecurityConfig  # Possible rename this to avoid confusing _config with _config_client

    _config_client: ConfigClient
    # _security_client: SecurityClient
    _nlp_client: NlpClient

    def __init__(self, sec_conf: SecurityConfig):
        self._configuration = sec_conf

        self._setup_clients()

    def _setup_clients(self, ):
        # Setup low-level clients
        self._config_client = ConfigClient(self._configuration)
        self._nlp_client = NlpClient(self._configuration)

    # todo remove? test purposes only
    def test_api(self):
        return self._config_client.test_api()

    def save_dataset(self, dataset_id: str, generator: typing.Generator, ):
        return self._nlp_client.save_dataset(dataset_id=dataset_id, generator=generator)


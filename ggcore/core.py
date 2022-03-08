import typing

from ggcore.api import AbstractApi
from ggcore.client import ConfigClient, SecurityClient, NlpClient
from ggcore.config import SecurityConfig
from ggcore.session import SdkSessionManager


class SdkCore:
    """
    SdkCore is the entrypoint for the backend of the SDK
    Drives initialization of clients and session, executes api calls

    SdkCore covers:
        - client creation
        - session manager creation
        - converting high-level "resource" calls into the low-level client calls
    """

    _configuration: SecurityConfig  # Possible rename this to avoid confusing _config with _config_client

    _config_client: ConfigClient
    _security_client: SecurityClient
    _nlp_client: NlpClient

    # static class for session management
    _session_manager: SdkSessionManager = SdkSessionManager

    def __init__(self, sec_conf: SecurityConfig):
        self._configuration = sec_conf

        self._setup_clients()
        self._setup_session()

    def _setup_clients(self, ):
        # Setup low-level clients
        self._config_client = ConfigClient(self._configuration)
        self._nlp_client = NlpClient(self._configuration)

    def _setup_session(self, ):
        pass
        # Setup Session Manager
        # self._session_manager.create_session(self._configuration)

    # def _invoke(self, api_req: AbstractApi):
    #     sdk_req = self._session_manager.build_sdk_request(api_req)
    #     return self._session_manager.execute_api_request(sdk_req)

    # todo remove? test purposes only
    def test_api(self):
        return self._config_client.test_api()

    def save_dataset(self, dataset_id: str, generator: typing.Generator, ):
        return self._nlp_client.save_dataset(dataset_id=dataset_id, generator=generator)


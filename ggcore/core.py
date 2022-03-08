import typing

from ggcore import http_base, client_factory
from ggcore.client import ConfigClient, SecurityClient, AbstractApi, NlpClient
from ggcore.config import SdkConfig
from ggcore.sdk_messages import SdkServiceResponse, SdkServiceRequest
from ggcore.security_base import SdkAuth
from ggcore.session import SdkSession, SdkSessionManager
from ggcore.utils import CONFIG, SECURITY, NLP


class SdkCore:
    """
    SdkCore is the entrypoint for setting up and making calls using the SDK

    SdkCore combines all the different pieces of the core including:
        - client creation
        - session creation
        - session state
        - calling the client apis by combining necessary parts (client call, session info, smart logic around these)
    """

    _config: SdkConfig # Possible rename this to avoid confusing _config with _config_client

    _config_client: ConfigClient
    _security_client: SecurityClient
    _nlp_client: NlpClient

    # static class for session management
    _session_manager: SdkSessionManager = SdkSessionManager

    def __init__(self, sdk_config: SdkConfig):
        self._config = SdkConfig(sdk_config)

        self._setup_clients()
        self._setup_session()


    def _setup_clients(self,):
        # Setup Config Client
        self._config_client = client_factory.client(CONFIG)
        self._security_client = client_factory.client(SECURITY)
        self._nlp_client = client_factory.client(NLP)

    def _setup_session(self,):
        # Setup Session
        self._session_manager.create_session(self._config)


    def _invoke(self,api_req: AbstractApi):
        sdk_req = self._session_manager.build_sdk_request(api_req)
        return self._session_manager.execute_api_request(sdk_req)

    def get_token(self):
        api_req = self._security_client.api_token_request()
        return self._invoke(api_req)

    def save_dataset(self, dataset_id: str, generator: typing.Generator,):
        api_req = self._nlp_client.api_for_save_dataset(dataset_id=dataset_id, generator=generator)
        return self._invoke( api_req )

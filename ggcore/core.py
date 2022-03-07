from ggcore import http_base, client_factory
from ggcore.client import ConfigClient, SecurityClient, AbstractApi
from ggcore.config import SdkConfig
from ggcore.sdk_messages import SdkServiceResponse, SdkServiceRequest
from ggcore.security_base import SdkAuth
from ggcore.session import SdkSession, SdkSessionFactory
from ggcore.utils import CONFIG, SECURITY


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

    _session: SdkSession

    def __init__(self, sdk_config: SdkConfig):
        self._config = SdkConfig(sdk_config)

        self._setup_clients()
        self._setup_session()


    def _setup_clients(self,):
        # Setup Config Client
        self._config_client = client_factory.client(CONFIG)
        self._security_client = client_factory.client(SECURITY)

    def _setup_session(self,):
        # Setup Session
        self._session = SdkSessionFactory.create_session(self._config)



    def call_api(self,api_request: AbstractApi):
        """
        missing items:
            - client_name for http


        can some of the duplication in this be removed? like we have to reference the auth type twice and http method type twice,
            can these be defined once with better/cleaner classes?
        """

        url_base = self._config.url_base()
        client_name = api_request.client_name()
        endpoint = api_request.endpoint()

        api_uri = f'http://{url_base}/1.0/{client_name}/{endpoint}'

        auth_header = SdkAuth(credentials=self._credentials).get_auth_for_http(auth_type=api_request.auth_type())

        sdk_request = SdkServiceRequest(endpoint=api_uri,
                                        request_auth_method=api_request.auth_type(),
                                        headers=auth_header,
                                        query_params=api_request.query_params())

        # --- MOVE ABOVE into a single SdkServiceRequest setup call? ----

        # Execute Request
        sdk_response: SdkServiceResponse = http_base.execute_request(sdk_request, api_request.http_method())

        # todo how does logic for expired tokens fit into this? does it make sense to have logic internal to this generic
        #   call or to have it wrap this somehow?
        #   logic:
            # if auth_type is bearer
                # check here if response code is for token
                # if not pass to handler
                # if it is then execute logic to get new token and retry request
            # if auth_type is basic then only can return the bad result.

        # Handle response
        return api_request.handler(sdk_response)




    def save_data(self):
        pass

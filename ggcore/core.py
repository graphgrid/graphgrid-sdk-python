from ggcore import http_base
from ggcore.client import ConfigClient, SecurityClient, AbstractApi
from ggcore.config import SdkConfig, URL_BASE
from ggcore.credentials import Credentials
from ggcore.sdk_exceptions import SdkInvalidConfigKey
from ggcore.sdk_messages import SdkServiceResponse, SdkServiceRequest
from ggcore.security_base import SdkAuth


class SdkCore:
    """
    SdkCore is the entrypoint for setting up and making calls using the SDK
    """

    _credentials: Credentials = None
    _config: SdkConfig

    _config_client: ConfigClient
    _security_client: SecurityClient

    def set_credentials(self, access_key, secret_key, token=None):
        self._credentials = Credentials(access_key, secret_key, token)

    def get_config(self, key):
        if key in self._config:
            return self._config[key]
        else:
            raise SdkInvalidConfigKey

    @property
    def credentials(self):
        return self._credentials

    def call_api(self,api_request: AbstractApi):
        """
        missing items:
            - client_name for http


        can some of the duplication in this be removed? like we have to reference the auth type twice and http method type twice,
            can these be defined once with better/cleaner classes?
        """

        url_base = self._config[URL_BASE]
        client_name = api_request.client_name()
        endpoint = api_request.endpoint()

        api_uri = f'http://{url_base}/1.0/{client_name}/{endpoint}'

        auth_header = SdkAuth(credentials=self._credentials).get_auth_for_http(auth_type=api_request.auth_type())

        sdk_request = SdkServiceRequest(endpoint=api_uri,
                                        request_auth_method=api_request.auth_type(),
                                        headers=auth_header,
                                        query_params=api_request.query_params())

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

    def refresh_credentials_token(self):
        token: str = self.call_api( self._security_client.api_token_request() )
        self._credentials.token = token




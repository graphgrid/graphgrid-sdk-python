"""

User does not interact with this session obj, instead the SessionCore is meant to hold state information about the current sdk

"""
from ggcore import http_base
from ggcore.client import SecurityClient, AbstractApi
from ggcore.config import SdkConfig
from ggcore.credentials import Credentials
from ggcore.sdk_messages import SdkServiceRequest, SdkServiceResponse
from ggcore.security_base import SdkAuth
from ggcore.utils import RequestAuthType

# does logic around the session and its creds/refresh-token reside within the SdkSession itself, or is it managed by something like the SdkCore?
class SdkSession:
    _credentials: Credentials
    is_authenticated_for_basic: bool = False
    is_authenticated_for_bearer: bool = False

    def __init__(self,credentials:Credentials):
        print("DEBUG: session setup")
        self._credentials = credentials

    @property
    def credentials(self):
        return self._credentials

    def __post_init_for_session__(self, security_client: SecurityClient):
        pass
        # if not self.is_authenticated_for_basic:
        #     self.__call_get_token(security_client)

    def __call_get_token(self, security_client: SecurityClient):
        pass
        # token = self.construct_service_request(security_client.api_token_request())

    def refresh_credentials_token(self):
        pass
        # token: str = self.call_api( self._security_client.api_token_request() )
        # self._credentials.token = token



class SdkSessionManager:
    """
    Manages the session and the logic around api calls it makes
    """

    _config: SdkConfig # config can be considered stateful, so can be stored alongside session
    _session: SdkSession

    @classmethod
    def create_session(cls, config: SdkConfig):
        cls._config = config

        if not cls._session:
            cls._session = SdkSession(Credentials(config.access_key(), config.secret_key()))

    @classmethod
    def build_sdk_request(cls, api_req: AbstractApi, ) -> SdkServiceRequest:
        sdk_req = SdkServiceRequest()  # will this result in error?

        # setting basic info for request
        sdk_req.endpoint = f'http://{cls._config.url_base()}/1.0/{api_req.client_name()}/{api_req.endpoint()}'

        headers = dict
        sdk_auth = SdkAuth(credentials=cls._session.credentials)

        # Set request_auth_method and add necessary headers
        if api_req.auth_type() == RequestAuthType.BASIC:
            sdk_req.request_auth_method = RequestAuthType.BASIC
            headers.update(sdk_auth.get_basic_header())

        elif api_req.auth_type() == RequestAuthType.BEARER:
            sdk_req.request_auth_method = RequestAuthType.BEARER
            headers.update(sdk_auth.get_bearer_header())

        # custom api headers
        sdk_req.headers = api_req.headers()

        sdk_req.http_method = api_req.http_method()
        sdk_req.query_params = api_req.query_params()
        sdk_req.body = api_req.body_fn()  # problematic?

        return sdk_req

    @classmethod
    def call_api_request(cls, sdk_request: SdkServiceRequest): # either need to pass in the abstract_api for the handler, or need to store the handler within the request? could that open up a way to have dynamically-user-defined handlers? does that even make sense?
        # --- wrap retry/smart logic around the request ---
        sdk_response: SdkServiceResponse = http_base.execute_request(sdk_request)
        # --- wrap retry/smart logic around the request ---



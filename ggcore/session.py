"""

User does not interact with this session obj, instead the SessionCore is meant to hold state information about the current sdk

"""
import enum

from ggcore import http_base
from ggcore.client import SecurityClient, AbstractApi
from ggcore.config import SdkConfig
from ggcore.credentials import Credentials
from ggcore.sdk_messages import SdkServiceRequest, SdkServiceResponse
from ggcore.security_base import SdkAuth
from ggcore.utils import RequestAuthType


# does logic around the session and its creds/refresh-token reside within the SdkSession itself, or is it managed by something like the SdkCore?
# need to wrap brain around/balance using the SdkSession and keeping track of state and using the GetTokenApi to handle certain codes like 404

# todo experimental WIP
class SessionState(enum.Enum):
    INITIAL = "INITIAL"
    WAIT_FOR_SECURITY = "WAIT_FOR_SECURITY"
    AUTH_SUCCESS_BASIC = "AUTH_SUCCESS_BASIC"
    AUTH_SUCCESS_BEARER = "AUTH_SUCCESS_BEARER"
    BAD_BASIC_AUTH = "BAD_BASIC_AUTH"

class SdkSession:
    _credentials: Credentials
    is_authenticated_for_basic: bool = False    # should only be false when a) startup before basic creds are tried b) the token req comes back 403
    is_authenticated_for_bearer: bool = False   # should only be true when the previous token call is successful
                                                # do we need two vars tracking this, or can it be logicked into a single one/ rework this to use true FSM (keep track of state)

    # using a set of static states of the SdkSession (as a FSM) may make sense here?
    _state: SessionState = SessionState.INITIAL

    def __init__(self,credentials:Credentials):
        print("DEBUG: session setup")
        self._credentials = credentials
        self._state = SessionState.WAIT_FOR_SECURITY

    @property
    def credentials(self):
        return self._credentials

    @property
    def state(self):
        return self._state

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
        cls._session = SdkSession(Credentials(config.access_key(), config.secret_key()))

    @classmethod
    def build_sdk_request(cls, api_req: AbstractApi, ) -> SdkServiceRequest:
        sdk_req = SdkServiceRequest()

        # setting basic info for request
        sdk_req.endpoint = f'http://{cls._config.url_base()}/1.0/{api_req.client_name()}/{api_req.endpoint()}'

        # custom api headers
        sdk_req.headers = api_req.headers()

        # authenticate (auth type+header)
        sdk_auth = SdkAuth(credentials=cls._session.credentials)
        if api_req.auth_type() == RequestAuthType.BASIC:
            sdk_req.request_auth_method = RequestAuthType.BASIC
            sdk_req.headers.update(sdk_auth.get_basic_header())
        elif api_req.auth_type() == RequestAuthType.BEARER:
            sdk_req.request_auth_method = RequestAuthType.BEARER
            sdk_req.headers.update(sdk_auth.get_bearer_header())

        # fill in sdk request from api request
        sdk_req.http_method = api_req.http_method()
        sdk_req.query_params = api_req.query_params()
        sdk_req.body = api_req.body()

        # higher-order function for response handler
        sdk_req.api_response_handler = api_req.handler

        return sdk_req

    @classmethod
    def execute_api_request(cls, sdk_request: SdkServiceRequest):
        sdk_response: SdkServiceResponse = http_base.execute_request(sdk_request)

        return sdk_request.api_response_handler(sdk_response)

    # todo WIP
    @classmethod
    def call(self):
        if self._session.state == SessionState.WAIT_FOR_SECURITY:
            pass
            # retry token call w/ backoff
        elif self._session.state == SessionState.AUTH_SUCCESS_BASIC:
            pass

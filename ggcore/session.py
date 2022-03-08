import enum

from ggcore import http_base
from ggcore.client import AbstractApi, SecurityClient
from ggcore.config import SdkConfig
from ggcore.credentials import Credentials
from ggcore.sdk_messages import SdkServiceRequest, SdkServiceResponse
from ggcore.security_base import SdkAuth
from ggcore.utils import RequestAuthType


# todo experimental WIP
class SessionState(enum.Enum):
    INITIAL = "INITIAL"
    WAIT_FOR_SECURITY = "WAIT_FOR_SECURITY" # todo do we even want the sdk waiting around for security? or if we get a 404 just bomb?
    AUTH_SUCCESS_BASIC = "AUTH_SUCCESS_BASIC"
    AUTH_SUCCESS_BEARER = "AUTH_SUCCESS_BEARER"
    ERROR_STATE = "ERROR_STATE"


class SdkSession:
    _credentials: Credentials
    is_authenticated_for_basic: bool = False    # should only be false when a) startup before basic creds are tried b) the token req comes back 403
    is_authenticated_for_bearer: bool = False   # should only be true when the previous token call is successful
                                                # do we need two vars tracking this, or can it be logicked into a single one/ rework this to use true FSM (keep track of state)

    # WIP using a set of static states of the SdkSession (as a FSM) may make sense here?
    _state: SessionState = SessionState.INITIAL
    _state_info: str = "No extra state info"   # extra info about the current state

    def __init__(self,credentials:Credentials):
        self._credentials = credentials
        self._state = SessionState.WAIT_FOR_SECURITY

    @property
    def credentials(self):
        return self._credentials

    @property
    def state(self):
        return self._state


class SdkSessionManager:
    """
    Manages the session and the logic around api calls it makes
    """

    _config: SdkConfig
    _session: SdkSession

    @classmethod
    def create_session(cls, config: SdkConfig):
        cls._config = config
        cls._session = SdkSession(Credentials(config.oauth_client_id(), config.oauth_client_secret()))

    @classmethod
    def build_sdk_request(cls, api_req: AbstractApi, ) -> SdkServiceRequest:
        sdk_req = SdkServiceRequest()

        # setting basic info for request
        sdk_req.endpoint = f'http://{cls._config.url_base()}/1.0/{api_req.api_base()}/{api_req.endpoint()}'

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

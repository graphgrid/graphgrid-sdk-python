"""

User does not interact with this session obj, instead the SessionCore is meant to hold state information about the current sdk

"""
from ggcore.client import SecurityClient, AbstractApi
from ggcore.config import SdkConfig
from ggcore.credentials import Credentials
from ggcore.sdk_messages import SdkServiceRequest
from ggcore.security_base import SdkAuth
from ggcore.utils import RequestAuthType

# does logic around the session and its creds/refresh-token reside within the SdkSession itself, or is it managed by something like the SdkCore?
class SdkSession:
    _credentials: Credentials
    is_authenticated_for_basic: bool = False
    is_authenticated_for_bearer: bool = False

    def __init__(self,sdk_config:SdkConfig):
        print("DEBUG: session setup")


    def __post_init_for_session__(self, security_client: SecurityClient):
        if not self.is_authenticated_for_basic:
            self.__call_get_token(security_client)

    # should the call_api be here instead of in core?
    # confusing myself because the session needs to get and track token, but the api calls are in the core

    def __call_get_token(self, security_client: SecurityClient):
        token = self.construct_service_request(security_client.api_token_request())

    def refresh_credentials_token(self):
        pass
        # token: str = self.call_api( self._security_client.api_token_request() )
        # self._credentials.token = token


    # def construct_service_request(self, aa: AbstractApi, k: UserRequestInfo): # and then UserRequestInfo could include things like custom headers/options to choose which endpoint the api should use?
    def construct_service_request(self, aa: AbstractApi):
        sdk_req = SdkServiceRequest()  # will this result in error?

        # setting basic info for request
        sdk_req.endpoint = aa.endpoint() # need to have a way to determine which endpoint an api should use dynamically? i.e. `/dataset/save` vs `/dataset/{id}/save` ?
        sdk_req.query_params = aa.query_params()
        sdk_req.body = aa.body_fn()  # problematic?

        headers = dict
        sdk_auth = SdkAuth(credentials=self._credentials)

        # Set Auth Type
        if aa.auth_type() == RequestAuthType.BASIC:
            sdk_req.request_auth_method = RequestAuthType.BASIC
            headers.update(sdk_auth.get_auth_for_http(auth_type=RequestAuthType.BASIC))

        elif aa.auth_type() == RequestAuthType.BEARER:
            sdk_req.request_auth_method = RequestAuthType.BEARER
            headers.update(sdk_auth.get_auth_for_http(auth_type=RequestAuthType.BEARER))

        # Set custom api headers?
        # todo custom api related headers set here? Is that something we actually need (YNGNI?)
        #   Will a way to construct custom headers based on the api call be needed?
        #    Will it need to be a mix of static api info and session/config info, or can we just get away with static api header info?


        return sdk_req


class SdkSessionFactory():
    @classmethod
    def create_session(cls, config: SdkConfig) -> SdkSession:
        # some way to check if session with the same bootstrap config already exists, and then return that one?
        return SdkSession(config)


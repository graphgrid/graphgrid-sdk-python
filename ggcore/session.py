"""

User does not interact with this session obj, instead the SessionCore is meant to hold state information about the current sdk

"""
from ggcore.client import SecurityClient
from ggcore.config import SdkConfig
from ggcore.credentials import Credentials


class SdkSession:
    _credentials: Credentials
    is_authenticated_for_basic: bool
    is_authenticated_for_bearer: bool

    def __init__(self,sdk_config:SdkConfig):
        print("DEBUG: session setup")
        print(f"DEBUG: url_base: {sdk_config.url_base()}")

    # should the call_api be here instead of in core?
    # confusing myself because the session needs to get and track token, but the api calls are in the core

    def __call_get_token(self):
        SecurityClient.GetTokenApi

    def refresh_credentials_token(self):
        pass
        # token: str = self.call_api( self._security_client.api_token_request() )
        # self._credentials.token = token





class SdkSessionFactory():
    @classmethod
    def create_session(cls, config: SdkConfig) -> SdkSession:
        # some way to check if session with the same bootstrap config already exists, and then return that one?
        return SdkSession(config)

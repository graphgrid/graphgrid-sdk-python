"""

User does not interact with this session obj, instead the SessionCore is meant to hold state information about the current sdk

"""
from ggcore.config import SdkConfig


class SdkSession:
    is_authenticated_for_basic: bool
    is_authenticated_for_bearer: bool



    def refresh_credentials_token(self):
        pass
        # token: str = self.call_api( self._security_client.api_token_request() )
        # self._credentials.token = token




class SdkSessionFactory():
    @classmethod
    def create_session(cls, config: SdkConfig) -> SdkSession:
        # some way to check if session with the same bootsrap config already exists, and then return that one?
        return SdkSession(config)

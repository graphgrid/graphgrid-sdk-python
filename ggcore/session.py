import enum
import typing

from ggcore.credentials import Credentials
from ggcore.sdk_messages import SdkServiceRequest
from ggcore.security_base import SdkAuth


# todo experimental WIP
class SessionState(enum.Enum):
    INITIAL = "INITIAL"
    UNABLE_TO_GET_TOKEN_403 = "UNABLE_TO_GET_TOKEN_403"     # bad basic auth
    UNABLE_TO_GET_TOKEN_404 = "UNABLE_TO_GET_TOKEN_404"     # security not up/bad url_base
    GOT_TOKEN_200 = "GOT_TOKEN_200"                         # got token
    ERROR_STATE = "ERROR_STATE"


class SdkSession:
    _state: SessionState = SessionState.INITIAL
    _state_info: str = "No extra state info"   # extra info about the current state

    @property
    def state(self):
        return self._state


class TokenFactory:
    _token_supplier: typing.Callable[[], str]

    def __init__(self, token_supp):
        self._token_supplier = token_supp

    def add_token_to_request(self, sdk_req: SdkServiceRequest):
        bearer_header = SdkAuth(
            Credentials(None, None, self.get_token_from_request())).get_bearer_header()  # SdkAuth needs reworked...
        sdk_req.headers.update(bearer_header)

    def get_token_from_request(self):
        return self._token_supplier()

"""Define classes around session tracking and token management."""
import time
import typing
from dataclasses import dataclass

from ggcore.sdk_exceptions import SdkBadOauthCredentials
from ggcore.sdk_messages import GetTokenResponse

# Buffer for token expiration timeout
TIMEOUT_BUFFER_SECONDS = 3


@dataclass
class TokenTracker:
    """Define class to keep track of token information."""
    token: str
    expires_in: int
    init_time: int


def get_time_in_ms():
    """Return current system time in ms"""
    return time.time_ns() // 1_000_000


class TokenFactory:
    """Define class to dynamically call for a token."""
    _token_supplier: typing.Callable[[], GetTokenResponse]

    _token_tracker: TokenTracker = None

    def __init__(self, token_supp):
        self._token_supplier = token_supp

    # pylint: disable=no-else-return
    def call_for_token(self):
        """Execute call to get a new token and populate the TokenTracker."""
        get_token_response = self._token_supplier()

        # 200 OK
        if get_token_response.status_code == 200:
            return TokenTracker(
                get_token_response.access_token,
                int(get_token_response.expires_in),  # cast expires_in to int
                get_time_in_ms()
            )

        # 401 Unauthorized
        elif get_token_response.status_code == 401:
            raise SdkBadOauthCredentials(
                'Security client returned "401 Unauthorized" when trying to '
                'get a token. Please check oauth credentials used by the SDK '
                'and retry.')

        else:
            raise RuntimeError(
                f'Unable to get security token but was not a 401 Unauthorized. '
                f'Status code: "{get_token_response.status_code}". Response: '
                f'"{get_token_response.response}")')

    def get_token(self) -> str:
        """Get token from the current TokenTracker."""
        return self._token_tracker.token

    def is_token_expired(self) -> bool:
        """Return whether current token has expired."""
        expiration_time = (self._token_tracker.init_time
                           + (self._token_tracker.expires_in * 1_000))
        return expiration_time - get_time_in_ms() <= TIMEOUT_BUFFER_SECONDS

    def is_token_present(self) -> bool:
        """Return whether there currently is a token."""
        return self._token_tracker is not None \
               and self._token_tracker.token is not None

    def is_token_ready(self):
        """Return whether the token is ready for use."""
        return self.is_token_present() and not self.is_token_expired()

    def token_handling(self) -> TokenTracker:
        """Return token"""
        if not self.is_token_ready():
            # token is not ready, request new token
            self.call_for_token()

        return self._token_tracker

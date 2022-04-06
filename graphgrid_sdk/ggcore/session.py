"""Define classes around session tracking and token management."""
import time
import typing
from dataclasses import dataclass

# Buffer for token expiration timeout
from graphgrid_sdk.ggcore.sdk_exceptions import \
    SdkInvalidOauthCredentialsException, SdkGetTokenException
from graphgrid_sdk.ggcore.sdk_messages import GetTokenResponse, \
    CheckTokenResponse

TIMEOUT_BUFFER_MS = 3000


def get_time_in_ms():
    """Return current system time in ms"""
    return time.time_ns() // 1_000_000


@dataclass
class TokenTracker:
    """Define class to keep track of token information."""
    token: str
    expires_in: int  # in milliseconds
    init_time: int = get_time_in_ms()


class TokenFactory:
    """Define class to dynamically call for a token."""
    _token_supplier: typing.Callable[[], GetTokenResponse]
    _token_checker: typing.Callable[[], CheckTokenResponse]

    _token_tracker: TokenTracker = None

    def __init__(self, token_supp, token_checker):
        self._token_supplier = token_supp
        self._token_checker = token_checker

    def call_get_token(self):
        """Execute call to get a new token and populate the TokenTracker."""
        get_token_response = self._token_supplier()

        # 200 OK
        if get_token_response.status_code == 200:
            self._token_tracker = TokenTracker(
                get_token_response.access_token,
                int(get_token_response.expires_in),  # cast expires_in to int
                get_time_in_ms()
            )

        # 401 Unauthorized
        elif get_token_response.status_code == 401:
            raise SdkInvalidOauthCredentialsException(
                'Unable to get security token. Get token endpoint returned '
                '"401 Unauthorized" using provided oauth credentials.')

        else:
            raise SdkGetTokenException(
                f'Unable to get security token. '
                f'Status code: "{get_token_response.status_code}". Response: '
                f'"{get_token_response.response}")')

        return self._token_tracker

    def call_check_token(self) -> CheckTokenResponse:
        """Execute call to check token and return response."""
        return self._token_checker()

    def get_current_token(self) -> str:
        """Get token from the current TokenTracker."""
        return self._token_tracker.token if self.is_token_present() else ""

    def is_token_expired(self) -> bool:
        """Return whether current token has expired."""
        expiration_time = (self._token_tracker.init_time
                           + self._token_tracker.expires_in)
        return expiration_time - get_time_in_ms() <= TIMEOUT_BUFFER_MS

    def is_token_present(self) -> bool:
        """Return whether there currently is a token."""
        return self._token_tracker is not None \
               and self._token_tracker.token is not None

    def is_token_ready(self) -> bool:
        """Return whether the token is ready for use."""
        return self.is_token_present() and not self.is_token_expired()

    def refresh_token(self, force_refresh=False) -> str:
        """Define method that conditionally refreshes the stored token.
        Returns the current token.
        """
        if force_refresh or not self.is_token_ready():
            # request new token
            self.call_get_token()

        return self.get_current_token()

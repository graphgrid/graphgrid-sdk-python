"""Define classes around session tracking and token management."""
import time
import typing
# pylint: disable=too-few-public-methods
from dataclasses import dataclass

from ggcore.sdk_messages import GetTokenResponse

TIMEOUT_BUFFER_SECONDS = 3


@dataclass
class TokenTracker:
    token: str
    expires_in: int
    init_time: int


def get_time_in_ms():
    return time.time_ns() // 1_000_000  # get current system time in ms


class TokenFactory:
    """Define class to dynamically call for a token."""
    _token_supplier: typing.Callable[[], GetTokenResponse]

    _token_tracker: TokenTracker

    def __init__(self, token_supp):
        self._token_supplier = token_supp

    def call_for_request_token(self):
        get_token_response = self._token_supplier()

        self._token_tracker = TokenTracker(
            get_token_response.access_token,
            int(get_token_response.expires_in),  # cast expires_in to int
            get_time_in_ms()
        )

        return self._token_tracker

    def get_token(self) -> str:
        """Get token from the current TokenTracker."""
        return self._token_tracker.token

    def is_token_expired(self) -> bool:
        expiration_time = (self._token_tracker.init_time
                           + (self._token_tracker.expires_in * 1_000))

        return expiration_time - get_time_in_ms() > TIMEOUT_BUFFER_SECONDS

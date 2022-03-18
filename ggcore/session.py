"""Define classes around session tracking and token management."""
import typing


# pylint: disable=too-few-public-methods
class TokenFactory:
    """Define class to dynamically call for a token."""
    _token_supplier: typing.Callable[[], str]

    def __init__(self, token_supp):
        self._token_supplier = token_supp

    def get_token_from_request(self) -> str:
        """Get token from the token supplier."""
        return self._token_supplier()

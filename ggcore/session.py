import typing


class TokenFactory:
    _token_supplier: typing.Callable[[], str]

    def __init__(self, token_supp):
        self._token_supplier = token_supp

    def get_token_from_request(self) -> str:
        """get token from the token supplier"""
        return self._token_supplier()

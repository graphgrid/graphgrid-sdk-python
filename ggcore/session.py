import typing


class TokenFactory:
    _token_supplier: typing.Callable[[], str]

    def __init__(self, token_supp):
        self._token_supplier = token_supp

    # maybe rename method since this supplier always gets and then stores the token?
    def get_token_from_request(self):
        return self._token_supplier()

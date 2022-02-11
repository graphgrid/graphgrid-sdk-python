import typing


class Credentials:
    access_key: typing.AnyStr
    secret_key: typing.AnyStr
    token: typing.AnyStr

    def __init__(self, access_key, secret_key, token=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = token

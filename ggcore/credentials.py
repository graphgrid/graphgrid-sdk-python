import typing


# todo how does Credentials and SecurityConfig mesh? Need to rewrite stuff and remove one? They overlap a lot
class Credentials:
    access_key: typing.AnyStr
    secret_key: typing.AnyStr
    token: typing.AnyStr

    def __init__(self, access_key, secret_key, token=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = token

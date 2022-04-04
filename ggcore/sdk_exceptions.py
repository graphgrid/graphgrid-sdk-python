"""Define sdk exception classes."""


class SdkException(Exception):
    """Define top level custom sdk exception."""


class SdkInvalidClient(SdkException):
    """Define exception for when the client requested is invalid."""


class SdkAuthTypeException(SdkException):
    """Define exception for when an invalid auth type is used."""


class SdkInvalidConfigKey(SdkException):
    """Define exception for when invalid config key is referenced."""


class SdkBadOauthCredentialsException(SdkException):
    """Define exception for when the base client credentials for getting a
    token are invalid.
    """


class SdkUnauthorizedWithValidTokenException(SdkException):
    """Define exception for when a sdk response is 401 Unauthorized
    but check_token is valid.
    """

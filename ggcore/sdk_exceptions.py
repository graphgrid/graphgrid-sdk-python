"""Define sdk exception classes."""


class SdkException(Exception):
    """Define top level custom sdk exception."""


class SdkInvalidClient(SdkException):
    """Define exception for when the client requested is invalid."""


class SdkAuthTypeException(SdkException):
    """Define exception for when an invalid auth type is used."""


class SdkInvalidConfigKey(SdkException):
    """Define exception for when invalid config key is referenced."""


class SdkGetTokenException(SdkException):
    """Define exception for when the sdk is unable to get a token."""


class SdkInvalidOauthCredentialsException(SdkGetTokenException):
    """Define exception for when the base client credentials for getting a
    token are invalid.
    """


class SdkUnauthorizedValidTokenException(SdkException):
    """Define exception for when a sdk response is 401 Unauthorized
    and current token is valid (check_token).
    """


class SdkUnauthorizedInvalidTokenException(SdkException):
    """Define exception for when a sdk response is 401 Unauthorized
    and current token is invalid (check_token).
    """

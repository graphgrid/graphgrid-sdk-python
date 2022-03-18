"""Define sdk exception classes."""


class SdkException(Exception):
    """Define top level custom sdk exception."""


class SdkInvalidClient(SdkException):
    """Define exception for when the client requested is invalid."""


class SdkAuthTypeException(SdkException):
    """Define exception for when an invalid auth type is used."""


class SdkInvalidConfigKey(SdkException):
    """Define exception for when invalid config key is referenced."""

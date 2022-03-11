class SdkException(Exception):
    """Top level custom sdk exception"""


class SdkInvalidClient(SdkException):
    """The client requested is invalid"""


class SdkAuthTypeException(SdkException):
    """Tried using an invalid auth type"""


class SdkInvalidConfigKey(SdkException):
    """Tried referencing an invalid config key"""

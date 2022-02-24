class SdkException(Exception):
    """ Top level custom sdk exception """


class SdkInvalidClient(Exception):
    """ The client requested is invalid """


class SdkAuthTypeException(Exception):
    """ Tried using an invalid auth type """


class SdkInvalidConfigKey(Exception):
    """ Tried referencing an invalid config key """

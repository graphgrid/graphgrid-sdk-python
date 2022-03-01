import dataclasses
from dataclasses import dataclass

from ggcore.utils import RequestAuthType


@dataclass
class SdkServiceRequest:
    endpoint: str
    # serviceUrl: str # see java sdk analog; used internally?

    request_auth_method: RequestAuthType

    headers: dict = dataclasses.field(default_factory=dict)
    query_params: dict = dataclasses.field(default_factory=dict)
    body: dict = dataclasses.field(default_factory=dict)

    # def __init__(self,):
    #     pass


    @endpoint.setter
    def endpoint(self, value):
        pass

    @request_auth_method.setter
    def request_auth_method(self, value):
        pass

    @headers.setter
    def headers(self, value):
        pass

    @body.setter
    def body(self, value):
        pass


@dataclass
class SdkServiceResponse:
    statusCode: int = None
    statusText: str = None

    response: dict = dataclasses.field(default_factory=dict)  # currently this is always a str, should it be a dict/can it somehow get mapped to a dict from a string?
    exception: Exception = None

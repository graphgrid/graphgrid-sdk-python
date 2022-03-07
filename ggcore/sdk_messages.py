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
    body: dict = dataclasses.field(default_factory=dict) # for the dataset_save this would be the generator passed in

    # def __init__(self,):
    #     pass


    @property
    def endpoint(self):
        return self.endpoint
    
    @endpoint.setter
    def endpoint(self, value):
        pass

    @property
    def request_auth_method(self):
        return self.request_auth_method

    @request_auth_method.setter
    def request_auth_method(self, value):
        pass

    @property
    def body(self):
        return self.body

    @body.setter
    def body(self, value):
        pass

    @property
    def headers(self):
        return self.headers

    @headers.setter
    def headers(self, value):
        pass

    @property
    def query_params(self):
        return self.query_params

    @query_params.setter
    def query_params(self, value):
        pass


@dataclass
class SdkServiceResponse:
    statusCode: int = None
    statusText: str = None

    response: dict = dataclasses.field(default_factory=dict)  # currently this is always a str, should it be a dict/can it somehow get mapped to a dict from a string?
    exception: Exception = None

class SavaDatasetResponse(SdkServiceResponse):
    dataset_id: str = None
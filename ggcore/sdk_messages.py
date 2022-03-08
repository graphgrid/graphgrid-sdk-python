import dataclasses
import typing
from dataclasses import dataclass

from ggcore.utils import RequestAuthType, HttpMethod


@dataclass
class SdkServiceResponse:
    statusCode: int = None
    statusText: str = None

    response: dict = dataclasses.field(default_factory=dict)  # currently this is always a str, should it be a dict/can it somehow get mapped to a dict from a string?
    exception: Exception = None


class SdkServiceRequest:
    _endpoint: str

    _http_method: HttpMethod

    _request_auth_method: RequestAuthType

    _headers: dict = {}#dataclasses.field(default_factory=dict)
    _query_params: dict = {}#dataclasses.field(default_factory=dict)
    _body: dict = {}#dataclasses.field(default_factory=dict)  # for the dataset_save this would be the generator passed in

    # default handler returns the SdkServiceResponse
    _api_response_handler: typing.Callable[[SdkServiceResponse], typing.Any] = lambda x: x

    # def __init__(self,):
    #     pass

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value

    @property
    def http_method(self):
        return self._http_method

    @http_method.setter
    def http_method(self, value: HttpMethod):
        self._http_method = value

    @property
    def request_auth_method(self):
        return self._request_auth_method

    @request_auth_method.setter
    def request_auth_method(self, value):
        self._request_auth_method = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        self._query_params = value

    @property
    def api_response_handler(self) -> typing.Callable[[SdkServiceResponse], typing.Any]:
        return self._api_response_handler

    @api_response_handler.setter
    def api_response_handler(self, value):
        self._api_response_handler = value

    def add_header(self, header_key, value, overwrite=True):
        if overwrite or (header_key not in self._headers):
            self._headers[header_key] = value


class SavaDatasetResponse(SdkServiceResponse):
    dataset_id: str = None

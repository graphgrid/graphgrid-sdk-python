import dataclasses
import typing
from dataclasses import dataclass

import requests

from ggcore.utils import HttpMethod


@dataclass
class SdkServiceResponse:
    statusCode: int = typing.Optional[int]
    statusText: str = typing.Optional[str]

    # is a str response here OK or does this need to be more generic/different?
    response: str = dataclasses.field(default_factory=str)

    exception: requests.RequestException = typing.Optional[
        requests.RequestException]


class SdkServiceRequest:
    # Full url used for the http request.
    #   Ex: 'http://localhost/1.0/security/oauth/token'
    _url: str

    # Endpoint constructed from the API definition (AbstractApi#api_base +
    # AbstractApi#endpoint).
    #   Ex: 'security/oauth/token'
    _api_endpoint: str

    # HttpMethod. Ex. GET
    _http_method: HttpMethod

    _headers: dict = {}
    _query_params: dict = {}
    _body: dict = {}

    # default handler returns the SdkServiceResponse
    _api_response_handler: typing.Callable[[SdkServiceResponse], typing.Any] \
        = lambda x: x

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def api_endpoint(self):
        return self._api_endpoint

    @api_endpoint.setter
    def api_endpoint(self, value):
        self._api_endpoint = value

    @property
    def http_method(self):
        return self._http_method

    @http_method.setter
    def http_method(self, value: HttpMethod):
        self._http_method = value

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
    def api_response_handler(self) -> typing.Callable[[SdkServiceResponse],
                                                      typing.Any]:
        return self._api_response_handler

    @api_response_handler.setter
    def api_response_handler(self, value):
        self._api_response_handler = value

    def add_header(self, header_key, value, overwrite=True):
        if overwrite or (header_key not in self._headers):
            self._headers[header_key] = value

    def add_headers(self, header_dict: dict, overwrite=True):
        for k, v in header_dict.items():
            self.add_header(k, v, overwrite)


class SavaDatasetResponse(SdkServiceResponse):
    dataset_id: str = None
    save_path: str = None

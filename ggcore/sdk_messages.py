"""Define classes for sdk service request/response objects."""

import dataclasses
import json
import typing
from dataclasses import dataclass

import requests

from ggcore.utils import HttpMethod


@dataclass
class SdkServiceResponse:
    """Define base class representing sdk service response."""

    status_code: int = typing.Optional[int]
    status_text: str = typing.Optional[str]

    # is a str response here OK or does this need to be more generic/different?
    response: str = dataclasses.field(default_factory=str)

    exception: requests.RequestException = typing.Optional[
        requests.RequestException]


# pylint: disable=too-many-instance-attributes
# pylint: disable=missing-function-docstring
class SdkServiceRequest:
    """Define base class representing sdk service request."""

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
        for key, value in header_dict.items():
            self.add_header(key, value, overwrite)

    def __eq__(self, other):
        if isinstance(other, SdkServiceRequest):
            return self._url == other._url \
                   and self._headers == other._headers \
                   and self._body == other._body \
                   and self._api_endpoint == other._api_endpoint \
                   and self._http_method == other._http_method \
                   and self._query_params == other._query_params \
                   and self._api_response_handler == self._api_response_handler
        return False


# pylint: disable=too-few-public-methods
class SaveDatasetResponse(SdkServiceResponse):
    """Define class representing a save dataset api call response."""
    dataset_id: str = None
    save_path: str = None


class PromoteModelResponse(SdkServiceResponse):
    """Define class representing a promote model api call response."""
    model_name: str
    task: str
    param_key: str


class PropertySource:
    """Define class representing a source of name/value property pairs."""

    def __init__(self, name: str, source: typing.Dict[typing.Any, typing.Any]):
        self.name = name
        self.source = source


# pylint: disable=too-many-arguments
class GetDataResponse(SdkServiceResponse):
    """Define class representing the environment response from get data."""
    def __init__(self, name: str, profiles: typing.List[str], label: str,
                 property_sources: typing.List[PropertySource], version: str,
                 state: str):
        self.name = name
        self.profiles = profiles
        self.label = label
        self.property_sources = [PropertySource(**property_source) for
                                 property_source in property_sources]
        self.version = version
        self.state = state


class TestApiResponse(SdkServiceResponse):
    """Define class representing a test api call response."""
    response_str: str = None

    # better way to populate? will all responses have to do this?
    def __init__(self, sdk_response: SdkServiceResponse):
        self.response = sdk_response.response
        self.status_text = sdk_response.status_text
        self.status_code = sdk_response.status_code
        self.exception = sdk_response.exception

        self.response_str = json.loads(self.response)["content"]


@dataclass
class GetJobStatusResponse(SdkServiceResponse):
    """Define class representing the get job status response"""
    dag_id: typing.Optional[str] = None
    dag_run_id: typing.Optional[str] = None
    start_date: typing.Optional[str] = None
    state: typing.Optional[str] = None


@dataclass
class GetJobResultsResponse(SdkServiceResponse):
    """Define class representing the get job status response"""
    dag_id: typing.Optional[str] = None
    dag_run_id: typing.Optional[str] = None
    start_date: typing.Optional[str] = None
    end_date: typing.Optional[str] = None
    state: typing.Optional[str] = None
    save_location: typing.Optional[str] = None


@dataclass
class JobTrainResponse(SdkServiceResponse):
    """Define class representing the job train response"""
    dag_run_id: typing.Optional[str] = None
    logical_date: typing.Optional[str] = None
    state: typing.Optional[str] = None

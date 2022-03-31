"""Define classes for sdk service request/response objects."""

import json
import typing

import requests

from ggcore.utils import HttpMethod


# pylint: disable=too-few-public-methods
class SdkResponseHelper:
    """Define helper class that serves as an inbetween for HTTP responses and
    SdkServiceResponses.
    """
    status_code: int
    status_text: str
    response: str
    exception: requests.RequestException

    def __init__(self, status_code=None, status_text=None, response=None,
                 exception=None):
        self.status_code = status_code
        self.status_text = status_text
        self.response = response
        self.exception = exception


# pylint: disable=too-few-public-methods
class SdkServiceResponse:
    """Define base class representing sdk service response."""

    status_code: typing.Optional[int] = None
    status_text: typing.Optional[str] = None
    response: typing.Optional[str] = None
    exception: typing.Optional[requests.RequestException] = None

    def __init__(self, sdk_response_obj: SdkResponseHelper):
        """Define method to init these base fields from SdkResponseHelper."""
        self.response = sdk_response_obj.response
        self.status_text = sdk_response_obj.status_text
        self.status_code = sdk_response_obj.status_code
        self.exception = sdk_response_obj.exception

    def __eq__(self, other):
        if isinstance(other, SdkServiceResponse):
            return self.response == other.response \
                   and self.status_code == other.status_code \
                   and self.status_text == other.status_text \
                   and self.exception == other.exception
        return False


# pylint: disable=too-many-instance-attributes
# pylint: disable=missing-function-docstring
class SdkServiceRequest:
    """Define base class representing sdk service request."""

    # Full url used for the http request.
    #   Ex: 'http://localhost/1.0/security/oauth/token'
    _url: str

    # Docker base used for the host address when in docker context.
    #   Ex: 'security'
    _docker_base: str

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
    _api_response_handler: typing.Callable[
        [SdkResponseHelper], SdkServiceResponse] \
        = lambda x: x

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def docker_base(self):
        return self._docker_base

    @docker_base.setter
    def docker_base(self, value):
        self._docker_base = value

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
    def api_response_handler(self) -> typing.Callable[[SdkResponseHelper],
                                                      SdkServiceResponse]:
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

    def __init__(self, sdk_response: SdkResponseHelper):
        super().__init__(sdk_response)

        loaded = json.loads(sdk_response.response)
        self.save_path = loaded['path']
        self.dataset_id = loaded['datasetId']


class PromoteModelResponse(SdkServiceResponse):
    """Define class representing a promote model api call response."""
    model_name: str
    task: str
    param_key: str

    def __init__(self, sdk_response: SdkResponseHelper):
        super().__init__(sdk_response)

        loaded = json.loads(sdk_response.response)
        self.model_name = loaded['modelName']
        self.task = loaded['task']
        self.param_key = loaded['paramKey']


class PropertySource:
    """Define class representing a source of name/value property pairs."""

    def __init__(self, name: str, source: typing.Dict[typing.Any, typing.Any]):
        self.name = name
        self.source = source


# pylint: disable=too-many-arguments
class GetDataResponse(SdkServiceResponse):
    """Define class representing the environment response from get data."""

    def __init__(self, sdk_response: SdkResponseHelper):
        super().__init__(sdk_response)

        loaded = json.loads(sdk_response.response)
        self.name = loaded["name"]
        self.profiles = loaded["profiles"]
        self.label = loaded["label"]
        self.property_sources = [PropertySource(**property_source) for
                                 property_source in loaded["propertySources"]]
        self.version = loaded["version"]
        self.state = loaded["state"]


class TestApiResponse(SdkServiceResponse):
    """Define class representing a test api call response."""
    response_str: str = None

    def __init__(self, sdk_response: SdkResponseHelper):
        super().__init__(sdk_response)

        loaded = json.loads(sdk_response.response)
        self.response_str = loaded['content']


class GetTokenResponse(SdkServiceResponse):
    """Define class representing a token call response."""
    access_token: str
    token_type: str
    expires_in: str
    created_at: str

    def __init__(self, sdk_response: SdkResponseHelper):
        super().__init__(sdk_response)

        loaded = json.loads(sdk_response.response)
        self.access_token = loaded['access_token']
        self.token_type = loaded['token_type']
        self.expires_in = loaded['expires_in']
        self.created_at = loaded['createdAt']

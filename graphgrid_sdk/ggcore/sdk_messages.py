"""Define classes for sdk service request/response objects."""

import json
import typing
from dataclasses import dataclass

import requests

from graphgrid_sdk.ggcore.utils import HttpMethod


# pylint: disable=too-few-public-methods
class GenericResponse:
    """Define class that HTTP responses are mapped into. Serves as an
    inbetween for HTTP responses and SdkServiceResponse subclasses.
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

    def __init__(self, generic_response: GenericResponse):
        """Define method to init these base fields from GenericResponse."""
        self.response = generic_response.response
        self.status_text = generic_response.status_text
        self.status_code = generic_response.status_code
        self.exception = generic_response.exception

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
                   and self._query_params == other._query_params
        return False


# pylint: disable=invalid-name
class DagRunResponse(SdkServiceResponse):
    """Define dag run response structure."""
    dagId: str
    dagRunId: str
    state: str
    startDate: str
    endDate: str
    logicalDate: str
    externalTrigger: bool
    conf: dict

    def __init__(self, generic_response: GenericResponse):
        super().__init__(generic_response)

        if self.status_code == 200:
            loaded: dict = json.loads(generic_response.response)
            self.dagId = loaded.get('dagId')
            self.dagRunId = loaded.get('dagRunId')
            self.state = loaded.get('state')
            self.startDate = loaded.get('startDate')
            self.endDate = loaded.get('endDate')
            self.logicalDate = loaded.get('logicalDate')
            self.externalTrigger = loaded.get('externalTrigger')
            self.conf = loaded.get('conf')


class NMTStatusResponse(DagRunResponse):
    """Define nlp model training status response."""
    savedModelName: str
    savedModelFilename: str
    savedModelUrl: str
    trainingAccuracy: float
    trainingLoss: float
    evalAccuracy: float
    evalLoss: float
    properties: dict

    def __init__(self, generic_response: GenericResponse):
        super().__init__(generic_response)

        if self.status_code == 200:
            loaded: dict = json.loads(generic_response.response)
            self.savedModelName = loaded.get("savedModelName")
            self.savedModelFilename = loaded.get("savedModelFilename")
            self.savedModelUrl = loaded.get("savedModelUrl")
            self.trainingAccuracy = loaded.get("trainingAccuracy")
            self.trainingLoss = loaded.get("trainingLoss")
            self.evalAccuracy = loaded.get("evalAccuracy")
            self.evalLoss = loaded.get("evalLoss")
            self.properties = loaded.get("properties")


class NMTTrainResponse(DagRunResponse):
    """Define nlp model training train response."""


# pylint: disable=too-few-public-methods
class SaveDatasetResponse(SdkServiceResponse):
    """Define class representing a save dataset api call response."""
    datasetId: str = None
    path: str = None

    def __init__(self, generic_response: GenericResponse):
        super().__init__(generic_response)

        loaded = json.loads(generic_response.response)
        self.path = loaded.get('path')
        self.datasetId = loaded.get('datasetId')


class PromoteModelResponse(SdkServiceResponse):
    """Define class representing a promote model api call response."""
    modelName: str
    task: str
    paramKey: str

    def __init__(self, generic_response: GenericResponse):
        super().__init__(generic_response)

        loaded = json.loads(generic_response.response)
        self.modelName = loaded.get('modelName')
        self.task = loaded.get('task')
        self.paramKey = loaded.get('paramKey')


class PropertySource:
    """Define class representing a source of name/value property pairs."""

    def __init__(self, name: str, source: typing.Dict[typing.Any, typing.Any]):
        self.name = name
        self.source = source


# pylint: disable=too-many-arguments
class GetDataResponse(SdkServiceResponse):
    """Define class representing the environment response from get data."""

    def __init__(self, generic_response: GenericResponse):
        super().__init__(generic_response)

        loaded = json.loads(generic_response.response)
        self.name = loaded.get('name')
        self.profiles = loaded.get('profiles')
        self.label = loaded.get('label')
        self.property_sources = [PropertySource(**property_source) for
                                 property_source in
                                 loaded.get('propertySources')]
        self.version = loaded.get('version')
        self.state = loaded.get('state')


class TestApiResponse(SdkServiceResponse):
    """Define class representing a test api call response."""
    response_str: str = None

    def __init__(self, generic_response: GenericResponse):
        super().__init__(generic_response)

        if self.status_code == 200:
            loaded = json.loads(generic_response.response)
            self.response_str = loaded.get('content')


class GetTokenResponse(SdkServiceResponse):
    """Define class representing a token call response."""
    access_token: str
    token_type: str
    expires_in: str
    created_at: str

    def __init__(self, generic_response: GenericResponse):
        super().__init__(generic_response)

        if self.status_code == 200:
            loaded = json.loads(generic_response.response)
            self.access_token = loaded.get('access_token')
            self.token_type = loaded.get('token_type')
            self.expires_in = loaded.get('expires_in')
            self.created_at = loaded.get('createdAt')


# pylint: disable=useless-super-delegation
class CheckTokenResponse(SdkServiceResponse):
    """Define class representing a check token call response."""

    def __init__(self, generic_response: GenericResponse):
        super().__init__(generic_response)


# pylint: disable=invalid-name
@dataclass
class TrainRequestBody:
    """Store Airflow configuration json/request bodies"""
    model: str
    datasets: typing.Union[dict, str]
    no_cache: bool = False
    GPU: bool = False

    def to_json(self):
        """Encode TrainRequestBody to a json object"""
        return json.dumps(self.__dict__, indent=4)


class GetActiveModelResponse(SdkServiceResponse):
    """Define class representing a get active model api call response."""
    task: str

    def __init__(self, generic_response: GenericResponse):
        super().__init__(generic_response)

        if self.status_code == 200:
            loaded: dict = json.loads(generic_response.response)
            self.model_name = loaded.get('modelName')
            self.trained_model_data = loaded.get('trainedModelData')

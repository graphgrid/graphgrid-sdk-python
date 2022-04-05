"""Define api related classes for the sdk."""
import typing
from dataclasses import dataclass

from ggcore.sdk_messages import SdkServiceRequest, \
    GetDataResponse, TestApiResponse, SaveDatasetResponse, GetTokenResponse, \
    SdkResponseHelper, PromoteModelResponse, SdkServiceResponse, \
    CheckTokenResponse
from ggcore.utils import CONFIG, SECURITY, NLP, HttpMethod, GRANT_TYPE_KEY, \
    GRANT_TYPE_CLIENT_CREDENTIALS, CONTENT_TYPE_HEADER_KEY, \
    CONTENT_TYPE_APP_JSON, USER_AGENT, CONTENT_TYPE_APP_X_WWW_FORM_URLENCODED


# pylint: disable=too-few-public-methods
class ApiGroup:
    """Define base class for abstract api groupings."""


class AbstractApi:
    """Define base class for abstract apis."""

    def api_base(self) -> str:
        """Return api_base ex. config, security, nlp."""

    def endpoint(self) -> str:
        """Return api endpoint."""

    def http_method(self) -> HttpMethod:
        """Return http method type."""

    # pylint: disable=no-self-use
    def headers(self) -> dict:
        """Return headers for the http request. Overriding impls should call super(
        ).headers() to get these default headers.
        """
        return {
            CONTENT_TYPE_HEADER_KEY: CONTENT_TYPE_APP_JSON,
            USER_AGENT: USER_AGENT
        }

    # pylint: disable=no-self-use
    def query_params(self) -> dict:
        """Return query params for the http request."""
        return {}  # overrides provide api-specific query-params

    # pylint: disable=no-self-use
    def body(self):
        """Return body of the http request."""
        return {}  # overrides provide api-specific body

    # pylint: disable=no-self-use
    def handler(self, sdk_response: SdkResponseHelper):
        """Handle the sdk response."""
        # default handler returns entire SdkResponseHelper
        return SdkServiceResponse(sdk_response)


class ConfigApi(ApiGroup):
    """Define grouping of Config api definitions."""

    @classmethod
    def test_api(cls, test_message: str = None):
        """Return test api."""
        return cls.TestApi(test_message)

    @classmethod
    def get_data_api(cls, module: str,
                     profiles: typing.Union[str, typing.List[str]],
                     revision: str):
        """Return get data api."""
        return cls.GetDataApi(module, profiles, revision)

    class TestApi(AbstractApi):
        """Define TestApi api."""
        _test_message: str

        def __init__(self, test_message):
            self._test_message = test_message

        def api_base(self) -> str:
            return CONFIG

        def endpoint(self) -> str:
            return "this/is/a/test"

        def http_method(self) -> HttpMethod:
            return HttpMethod.GET

        def handler(self, sdk_response: SdkResponseHelper):
            return TestApiResponse(sdk_response)

    class GetDataApi(AbstractApi):
        """Define GetDataApi api."""
        _module: str
        _profiles: typing.Union[str, typing.List[str]]
        _revision: str

        def __init__(self, module: str,
                     profiles: typing.Union[str, typing.List[str]],
                     revision: str):
            self._module = module
            self._profiles = profiles
            self._profiles = ",".join(self._profiles) if isinstance(
                self._profiles, list) else self._profiles
            self._revision = revision

        def api_base(self) -> str:
            return CONFIG

        def endpoint(self):
            return f"data/{self._module}/{self._profiles}/{self._revision}"

        def http_method(self) -> HttpMethod:
            return HttpMethod.GET

        def handler(self, sdk_response: SdkResponseHelper):
            return GetDataResponse(sdk_response)


class SecurityApi(ApiGroup):
    """Define grouping of Security api definitions."""

    @classmethod
    def get_token_api(cls):
        """Return get token api."""
        return cls.GetTokenApi()

    @classmethod
    def check_token_api(cls, token: str):
        """Return check token api."""
        return cls.CheckTokenApi(token)

    class GetTokenApi(AbstractApi):
        """Define GetTokenApi api."""

        def api_base(self):
            return SECURITY

        def endpoint(self):
            return "oauth/token"

        def http_method(self) -> HttpMethod:
            return HttpMethod.POST

        def query_params(self) -> dict:
            return {GRANT_TYPE_KEY: GRANT_TYPE_CLIENT_CREDENTIALS}

        def handler(self, sdk_response: SdkResponseHelper):
            return GetTokenResponse(sdk_response)

    class CheckTokenApi(AbstractApi):
        """Define CheckTokenApi api."""

        _token: str

        def __init__(self, token: str):
            self._token = token if token else ""

        def api_base(self):
            return SECURITY

        def endpoint(self):
            return "oauth/check_token"

        def http_method(self) -> HttpMethod:
            return HttpMethod.POST

        def query_params(self) -> dict:
            return {GRANT_TYPE_KEY: GRANT_TYPE_CLIENT_CREDENTIALS}

        def body(self):
            return {"token": self._token}

        def headers(self) -> dict:
            return {
                CONTENT_TYPE_HEADER_KEY: CONTENT_TYPE_APP_X_WWW_FORM_URLENCODED
            }

        def handler(self, sdk_response: SdkResponseHelper):
            return CheckTokenResponse(sdk_response)


class NlpApi(ApiGroup):
    """Define grouping of Nlp api definitions."""

    @classmethod
    def save_dataset_api(cls, generator: typing.Generator, dataset_id: str,
                         overwrite: bool):
        """Return save dataset api."""
        return cls.SaveDatasetApi(generator, dataset_id, overwrite)

    @classmethod
    def promote_model_api(cls, model_name: str, nlp_task: str,
                          environment: str):
        """Return promote model api."""
        return cls.PromoteModelApi(model_name, nlp_task, environment)

    @dataclass
    class SaveDatasetApi(AbstractApi):
        """Define SaveDatasetApi api."""
        _generator: typing.Generator
        _dataset_id: str
        _overwrite: bool

        def __init__(self, generator: typing.Generator, dataset_id: str,
                     overwrite: bool):
            self._generator = generator
            self._dataset_id = dataset_id
            self._overwrite = overwrite

        def api_base(self) -> str:
            return NLP

        def endpoint(self):
            return f"dataset{'/' + self._dataset_id if self._dataset_id else ''}/save"

        def http_method(self) -> HttpMethod:
            return HttpMethod.POST

        def query_params(self) -> dict:
            return {"overwrite": "true"} if self._overwrite else {}

        def body(self):
            return self._generator

        def handler(self, sdk_response: SdkResponseHelper):
            return SaveDatasetResponse(sdk_response)

    @dataclass
    class PromoteModelApi(AbstractApi):
        """Define PromoteModelApi api."""
        _model_name: str
        _nlp_task: str
        _environment: str

        def __init__(self, model_name: str, nlp_task: str, environment: str):
            self._model_name = model_name
            self._nlp_task = nlp_task
            self._environment = environment

        def api_base(self) -> str:
            return NLP

        def endpoint(self):
            return f"promoteModel/{self._environment}/{self._nlp_task}/{self._model_name}"

        def http_method(self) -> HttpMethod:
            return HttpMethod.POST

        def handler(self, sdk_response: SdkResponseHelper):
            return PromoteModelResponse(sdk_response)


class SdkRequestBuilder:
    """Define helper class for building sdk requests."""

    @classmethod
    def build_partial_sdk_request(cls,
                                  api_def: AbstractApi) -> SdkServiceRequest:
        """Build partial sdk request from an api definition."""
        sdk_req = SdkServiceRequest()

        sdk_req.docker_base = api_def.api_base()
        sdk_req.api_endpoint = f'{api_def.api_base()}/{api_def.endpoint()}'
        sdk_req.headers = api_def.headers()
        sdk_req.http_method = api_def.http_method()
        sdk_req.query_params = api_def.query_params()
        sdk_req.body = api_def.body()

        # handler function reference
        sdk_req.api_response_handler = api_def.handler

        return sdk_req

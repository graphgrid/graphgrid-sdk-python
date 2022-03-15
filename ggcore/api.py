"""Api related classes for the sdk."""
import json
import typing
from dataclasses import dataclass

from ggcore.sdk_messages import SdkServiceResponse, SdkServiceRequest
from ggcore.utils import CONFIG, SECURITY, NLP, HttpMethod, GRANT_TYPE_KEY, \
    GRANT_TYPE_CLIENT_CREDENTIALS, CONTENT_TYPE_HEADER_KEY, \
    CONTENT_TYPE_APP_JSON, USER_AGENT


# pylint: disable=too-few-public-methods
class ApiGroup:
    """Abstract api grouping"""


class AbstractApi:
    """Abstract api class"""

    def api_base(self) -> str:
        """Get api_base ex. config, security, nlp"""

    def endpoint(self) -> str:
        """Api endpoint"""

    def http_method(self) -> HttpMethod:
        """Http method type"""

    # pylint: disable=no-self-use
    def headers(self) -> dict:
        """Provides headers for the http request. Overriding impls should call super(
        ).headers() to get these default headers """
        return {
            CONTENT_TYPE_HEADER_KEY: CONTENT_TYPE_APP_JSON,
            USER_AGENT: USER_AGENT
        }

    # pylint: disable=no-self-use
    def query_params(self) -> dict:
        """Query params for the http request"""
        return {}  # overrides provide api-specific query-params

    # pylint: disable=no-self-use
    def body(self):
        """Body of the http request"""
        return {}  # overrides provide api-specific body

    # pylint: disable=no-self-use
    def handler(self, sdk_response: SdkServiceResponse):
        """Handler for the sdk response"""
        return sdk_response  # default handler returns entire SdkServiceResponse


class ConfigApi(ApiGroup):
    """Config api definitions"""

    @classmethod
    def test_api(cls):
        """Returns test api"""
        return cls.TestApi()

    @classmethod
    def get_data_api(cls):
        """Returns get data api"""
        return cls.GetDataApi()

    class TestApi(AbstractApi):
        """TestApi api definition"""

        def api_base(self) -> str:
            return CONFIG

        def endpoint(self) -> str:
            return "this/is/a/test"

        def http_method(self) -> HttpMethod:
            return HttpMethod.get

    class GetDataApi(AbstractApi):
        """GetDataApi api definition"""

        def api_base(self) -> str:
            return CONFIG

        def endpoint(self):
            return "data"

        def http_method(self) -> HttpMethod:
            return HttpMethod.get


class SecurityApi(ApiGroup):
    """Security api definitions"""

    @classmethod
    def get_token_api(cls):
        """Returns get token api"""
        return cls.GetTokenApi()

    class GetTokenApi(AbstractApi):
        """GetTokenApi api definition"""

        def api_base(self):
            return SECURITY

        def endpoint(self):
            return "oauth/token"

        def http_method(self) -> HttpMethod:
            return HttpMethod.post

        def query_params(self) -> dict:
            return {GRANT_TYPE_KEY: GRANT_TYPE_CLIENT_CREDENTIALS}

        def handler(self, sdk_response: SdkServiceResponse):
            # todo how does this handler play into the token tracking?
            if sdk_response.statusCode != 200:
                raise RuntimeError(
                    f'Unable to get security token. Response: "{sdk_response.response}"')

            # parse response
            json_acceptable_string = sdk_response.response.replace("'", "\"")
            return json.loads(json_acceptable_string)["access_token"]


class NlpApi(ApiGroup):
    """Nlp api definitions"""

    @classmethod
    def save_dataset_api(cls, generator: typing.Generator, dataset_id: str,
                         overwrite: bool):
        """Returns save dataset api"""
        return cls.SaveDatasetApi(generator, dataset_id, overwrite)

    @dataclass
    class SaveDatasetApi(AbstractApi):
        """SaveDatasetApi api definition"""
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
            return HttpMethod.post

        def query_params(self) -> dict:
            return {"overwrite": "true"} if self._overwrite else {}

        def body(self):
            return self._generator

        def handler(self, sdk_response: SdkServiceResponse):
            return sdk_response


class SdkRequestBuilder:
    """Helper class for building sdk requests"""

    @classmethod
    def build_partial_sdk_request(cls,
                                  api_def: AbstractApi) -> SdkServiceRequest:
        """Build partial sdk request from an api definition"""
        sdk_req = SdkServiceRequest()

        sdk_req.api_endpoint = f'{api_def.api_base()}/{api_def.endpoint()}'
        sdk_req.headers = api_def.headers()
        sdk_req.http_method = api_def.http_method()
        sdk_req.query_params = api_def.query_params()
        sdk_req.body = api_def.body()

        # handler function reference
        sdk_req.api_response_handler = api_def.handler

        return sdk_req

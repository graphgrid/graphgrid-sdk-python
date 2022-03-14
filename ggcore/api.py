import json
import typing
from dataclasses import dataclass

from ggcore.sdk_messages import SdkServiceResponse, SdkServiceRequest
from ggcore.utils import CONFIG, SECURITY, NLP, HttpMethod, GRANT_TYPE_KEY, \
    GRANT_TYPE_CLIENT_CREDENTIALS, CONTENT_TYPE_HEADER_KEY, \
    CONTENT_TYPE_APP_JSON, USER_AGENT


class ApiGroup:
    pass


class AbstractApi:
    def api_base(self) -> str:
        pass

    def endpoint(self) -> str:
        pass

    def http_method(self) -> HttpMethod:
        pass

    # overriding impls should call super().headers() to get these default
    # headers
    def headers(self) -> dict:
        return {
            CONTENT_TYPE_HEADER_KEY: CONTENT_TYPE_APP_JSON,
            USER_AGENT: USER_AGENT
        }

    def query_params(self) -> dict:
        return {}  # overrides provide api-specific query-params

    def body(self):
        return {}  # overrides provide api-specific body

    def handler(self, sdk_response: SdkServiceResponse):
        return sdk_response  # default handler returns entire SdkServiceResponse


class ConfigApi(ApiGroup):

    @classmethod
    def test_api(cls):
        return cls.TestApi()

    @classmethod
    def get_data_api(cls):
        return cls.GetDataApi()

    class TestApi(AbstractApi):
        def api_base(self) -> str:
            return CONFIG

        def endpoint(self) -> str:
            return "this/is/a/test"

        def http_method(self) -> HttpMethod:
            return HttpMethod.get

    class GetDataApi(AbstractApi):
        def api_base(self) -> str:
            return CONFIG

        def endpoint(self):
            return "data"

        def http_method(self) -> HttpMethod:
            return HttpMethod.get


class SecurityApi(ApiGroup):
    @classmethod
    def get_token_api(cls):
        return cls.GetTokenApi()

    class GetTokenApi(AbstractApi):
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
    @classmethod
    def save_dataset_api(cls, generator: typing.Generator, dataset_id: str,
                         overwrite: bool):
        return cls.SaveDatasetApi(generator, dataset_id, overwrite)

    @dataclass
    class SaveDatasetApi(AbstractApi):
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
    @classmethod
    def build_partial_sdk_request(cls,
                                  api_req: AbstractApi) -> SdkServiceRequest:
        sdk_req = SdkServiceRequest()

        sdk_req.api_endpoint = f'{api_req.api_base()}/{api_req.endpoint()}'
        sdk_req.headers = api_req.headers()
        sdk_req.http_method = api_req.http_method()
        sdk_req.query_params = api_req.query_params()
        sdk_req.body = api_req.body()

        # handler function reference
        sdk_req.api_response_handler = api_req.handler

        return sdk_req

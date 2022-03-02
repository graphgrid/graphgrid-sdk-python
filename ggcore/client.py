import json
from dataclasses import dataclass

from ggcore import http_base
from ggcore.credentials import Credentials
from ggcore.sdk_messages import SdkServiceRequest, SdkServiceResponse
from ggcore.security_base import SdkAuth
from ggcore.utils import CONFIG, SECURITY, NLP, RequestAuthType, HttpMethod, GRANT_TYPE_KEY, \
    GRANT_TYPE_CLIENT_CREDENTIALS


class GraphGridModuleClient:
    """
    client_name: subclass defined; static name of the client
    """
    _client_name: str

    def client_name(self) -> str:
        pass


class AbstractApi:
    # currently making it so each api can reference the client its contained in, is this the right pattern here?
    _client: GraphGridModuleClient

    def __init__(self, client: GraphGridModuleClient):
        self._client = client

    def endpoint(self) -> str:
        pass

    def auth_type(self) -> RequestAuthType:
        pass

    def http_method(self) -> HttpMethod:
        pass

    def query_params(self) -> dict:
        pass

    def handler(self, sdk_response: SdkServiceResponse):
        pass

    def client_name(self):
        self._client.client_name()


class ConfigClient(GraphGridModuleClient):
    _client_name = CONFIG

    @property
    def client_name(self):
        return self._client_name

    # todo being depricated
    def get_data(self, path: str) -> str:
        endpoint = self._http_base() + "data"

        # how does the security token even get in for this call? this is why we need to separate the client apis from the request creation and execution itself
        # could setup a call_api method that takes two functions (or just one?) as input, and then pass these `get_data` apis back which returns an obj containing the endpoint and a handler
        # for what to do with the output of the request

    class GetDataApi(AbstractApi):
        def endpoint(self):
            return "data"

        def auth_type(self) -> RequestAuthType:
            return RequestAuthType.BEARER

        def handler(self):
            pass


class SecurityClient(GraphGridModuleClient):
    _client_name = SECURITY

    @property
    def client_name(self):
        return self._client_name

    def api_token_request(self):
        return self.GetTokenApi(self)

    @dataclass
    class GetTokenApi(AbstractApi):

        def __init__(self, client: GraphGridModuleClient):
            super().__init__(client)

        def endpoint(self):
            return "oauth/token"

        def auth_type(self) -> RequestAuthType:
            return RequestAuthType.BASIC

        def http_method(self) -> HttpMethod:
            return HttpMethod.post

        def query_params(self) -> dict:
            return {GRANT_TYPE_KEY: GRANT_TYPE_CLIENT_CREDENTIALS}

        def handler(self, sdk_response: SdkServiceResponse):
            # todo add test for non-200 status
            if sdk_response.statusCode != 200:
                raise RuntimeError(f'Unable to get security token. Response: "{sdk_response.response}"')

            # parse response
            json_acceptable_string = sdk_response.response.replace("'", "\"")
            return json.loads(json_acceptable_string)["access_token"]


    # todo getting depricated
    def get_token(self, creds: Credentials):
        # endpoint
        endpoint = self._http_base() + "oauth/token"

        # todo Can the SdkAuth just be made automatically or something? Cumbersome to manually create the headers and set them
        # construct sdk request
        headers = SdkAuth(credentials=creds).get_auth_for_http(auth_type=RequestAuthType.BASIC)
        sdk_request = SdkServiceRequest(endpoint=endpoint, headers=headers, request_auth_method=RequestAuthType.BASIC)

        # Set grant type
        sdk_request.query_params[GRANT_TYPE_KEY] = GRANT_TYPE_CLIENT_CREDENTIALS

        # Execute Request
        sdk_response: SdkServiceResponse = http_base.execute_request(sdk_request, HttpMethod.post)

        # todo add test for non-200 status
        if sdk_response.statusCode != 200:
            raise RuntimeError(f'Unable to get security token. Response: "{sdk_response.response}"')

        # parse response
        response:str = sdk_response.response
        json_acceptable_string = response.replace("'", "\"")
        token = json.loads(json_acceptable_string)["access_token"]

        return token


class NlpClient(GraphGridModuleClient):
    _client_name = NLP

    @property
    def client_name(self):
        return self._client_name

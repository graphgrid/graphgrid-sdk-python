import json

from ggcore import http_base
from ggcore.credentials import Credentials
from ggcore.sdk_messages import SdkServiceRequest, SdkServiceResponse
from ggcore.security_base import SdkAuth
from ggcore.utils import CONFIG, SECURITY, NLP, RequestAuthType, HttpMethod, GRANT_TYPE_KEY, \
    GRANT_TYPE_CLIENT_CREDENTIALS


class GraphGridModuleClient:
    """
    url_base: address of client (ex. "localhost", "gg-dev")
    client_name: subclass defined; static name of the client
    """
    _url_base: str
    _client_name: str

    def is_available(self):
        pass

    def client_name(self):
        pass

    def url_base(self):
        pass

    # Should construction of http reqs be moved into their own class? Disconnected from the client obj itself?
    def _http_base(self):
        return f'http://{self._url_base}/1.0/{self.client_name}/'

    def __init__(self, url_base):
        self._url_base = url_base


class ConfigClient(GraphGridModuleClient):
    _client_name = CONFIG

    def __init__(self, url_base):
        super().__init__(url_base)

    @property
    def client_name(self):
        return self._client_name

    @property
    def url_base(self):
        return self._url_base



    def get_data(self, path: str) -> str:
        endpoint = self._http_base() + "data"

        # how does the security token even get in for this call? this is why we need to separate the client apis from the request creation and execution itself
            # could setup a call_api method that takes two functions (or just one?) as input, and then pass these `get_data` apis back which returns an obj containing the endpoint and a handler
            # for what to do with the output of the request


    class GetDataRequest():
        def endpoint(self):
            return "data"

        def handler(self):
            pass

class SecurityClient(GraphGridModuleClient):
    _client_name = SECURITY

    _ENDPOINTS = {
        "OAUTH_TOKEN": "oauth/token"
    }

    def __init__(self, url_base):
        super().__init__(url_base)

    @property
    def client_name(self):
        return self._client_name

    @property
    def url_base(self):
        return self._url_base


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

    def __init__(self, url_base):
        super().__init__(url_base)

    @property
    def client_name(self):
        return self._client_name

    @property
    def url_base(self):
        return self._url_base

    def save(self):
        pass






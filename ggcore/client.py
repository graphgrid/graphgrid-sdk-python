import json
from dataclasses import dataclass

from ggcore.sdk_messages import SdkServiceResponse
from ggcore.utils import CONFIG, SECURITY, NLP, RequestAuthType, HttpMethod, GRANT_TYPE_KEY, \
    GRANT_TYPE_CLIENT_CREDENTIALS


class GraphGridModuleClient:
    """
    client_name: subclass defined; static name of the client
    """
    _client_name: str

    # this is being used as the api path within the api base, i.e. `http://localhost/{client_name}/...`. this kidna makes sense, but could we achieve this without having to pass in clients into the api innerclassses?
    def client_name(self) -> str:
        pass


class AbstractApi:
    # currently making it so each api can reference the client its contained in, is this the right pattern here?
    _client: GraphGridModuleClient

    def __init__(self, client: GraphGridModuleClient):
        self._client = client

    # What about the cases where there are multiple possible endpoints for a single api (ie. dataset save with/without a name)?
    def endpoint(self) -> str:
        pass

    def auth_type(self) -> RequestAuthType:
        pass

    def http_method(self) -> HttpMethod:
        pass

    def query_params(self) -> dict:
        pass

    def body_fn(self): # needs fleshed out...?
        return lambda x: None

    def handler(self, sdk_response: SdkServiceResponse):
        pass

    def client_name(self):
        self._client.client_name()


class ConfigClient(GraphGridModuleClient):
    _client_name = CONFIG

    @property
    def client_name(self):
        return self._client_name

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


class NlpClient(GraphGridModuleClient):
    _client_name = NLP

    @property
    def client_name(self):
        return self._client_name

    @dataclass
    class SaveDatasetApi(AbstractApi):

        def __init__(self, client: GraphGridModuleClient):
            super().__init__(client)

        def endpoint(self):
            return "dataset/save"
            # how would this account for multiple endpoints like `dataset/{name}/save`

        # def endpoint(self, dataset_id):
        #     return "dataset/save" if not dataset_id else return f'dataset/{dataset_id}/save'
        #     # how would this account for multiple endpoints like `dataset/{name}/save`

        def auth_type(self) -> RequestAuthType:
            return RequestAuthType.BEARER

        def http_method(self) -> HttpMethod:
            return HttpMethod.post

        def query_params(self) -> dict:
            pass

        def handler(self, sdk_response: SdkServiceResponse):
            # todo add test for non-200 status
            if sdk_response.statusCode != 200:
                raise RuntimeError(f'Unable to get security token. Response: "{sdk_response.response}"')

            # parse response
            json_acceptable_string = sdk_response.response.replace("'", "\"")
            return json.loads(json_acceptable_string)["access_token"]

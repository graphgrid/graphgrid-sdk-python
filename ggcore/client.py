from ggcore.api import SecurityApi, SdkRequestBuilder, NlpApi, ConfigApi
from ggcore.config import SecurityConfig
from ggcore.http_base import SdkHttpClient
from ggcore.sdk_messages import SdkServiceResponse, SdkServiceRequest
from ggcore.session import TokenFactory


class ClientBase:
    security_conf: SecurityConfig

    def __init__(self, sec_conf):
        self.security_conf = sec_conf

    def make_request(self, sdk_req: SdkServiceRequest) -> SdkServiceResponse:
        return SdkHttpClient.invoke(sdk_req)


class SecurityClient(ClientBase):
    def get_token(self):
        sdk_request = SdkRequestBuilder.build_sdk_request(SecurityApi.get_token_api(), self.security_conf)
        return self.make_request(sdk_request)


class SecurityClientBase(ClientBase):
    _security_client: SecurityClient
    _token_factory: TokenFactory

    def __init__(self,sec_conf):
        self.security_conf = sec_conf
        self.configure_security()

    def configure_security(self, ):
        self._security_client = SecurityClient(self.security_conf)
        self._token_factory = TokenFactory(self._security_client.get_token)

    def make_request(self, sdk_req: SdkServiceRequest) -> SdkServiceResponse:
        self._token_factory.add_token_to_request(sdk_req)
        return super().make_request(sdk_req)


class ConfigClient(SecurityClientBase):
    def test_api(self):
        api_call = ConfigApi.test_api()
        sdk_request = SdkRequestBuilder.build_sdk_request(api_call, self.security_conf)
        return self.make_request(sdk_request)


class NlpClient(SecurityClientBase):
    def save_dataset(self, dataset_id, generator):
        api_call = NlpApi.save_dataset_api(dataset_id, generator)
        sdk_request = SdkRequestBuilder.build_sdk_request(api_call, self.security_conf)
        return self.make_request(sdk_request)



from ggcore.api import SecurityApi, SdkRequestBuilder, NlpApi, ConfigApi
from ggcore.config import SdkBootstrapConfig, SdkSecurityConfig
from ggcore.http_base import SdkHttpClient
from ggcore.sdk_messages import SdkServiceResponse, SdkServiceRequest
from ggcore.security_base import SdkAuth
from ggcore.session import TokenFactory
from ggcore.utils import RequestAuthType


class ClientBase:
    _bootstrap_config: SdkBootstrapConfig

    def __init__(self, bootstrap_config):
        self._bootstrap_config = bootstrap_config

    def make_request(self, sdk_req: SdkServiceRequest) -> SdkServiceResponse:
        # apply url base to sdk endpoint
        sdk_req.endpoint = f'http://{self._bootstrap_config.url_base}/1.0/{sdk_req.endpoint}'
        return SdkHttpClient.invoke(sdk_req)


class SecurityClient(ClientBase):

    _security_config: SdkSecurityConfig


    def __init__(self, bootstrap_config):
        super().__init__(bootstrap_config)
        self._security_config = SdkSecurityConfig(bootstrap_config)

    def request_and_store_token(self):
        sdk_request = SdkRequestBuilder.build_sdk_request(SecurityApi.get_token_api())

        sdk_request.request_auth_method = RequestAuthType.BASIC

        auth_basic_header = SdkAuth.get_basic_header(self._security_config)
        sdk_request.headers.update(auth_basic_header)

        token = self.make_request(sdk_request)

        self._security_config.token = token

        return token

    def is_token_present(self):
        return True if self._security_config.token else False

    @property
    def security_config(self):
        return self._security_config


class SecurityClientBase(ClientBase):
    _security_client: SecurityClient
    _token_factory: TokenFactory

    def __init__(self,bootstrap_conf):
        super().__init__(bootstrap_conf)

        # Configure security client and token factory
        self._security_client = SecurityClient(self._bootstrap_config)
        self._token_factory = TokenFactory(self._security_client.request_and_store_token)

    def make_request(self, sdk_req: SdkServiceRequest) -> SdkServiceResponse:

        # todo Add support for getting new token when the present one expires
        # very basic token management, gets token once then uses that
        if not self._security_client.is_token_present():
            # token not present, so get and store it
            self._token_factory.get_token_from_request()

        # add token header to request
        sdk_req.add_headers(SdkAuth.get_bearer_header(self._security_client.security_config))

        return super().make_request(sdk_req)


class ConfigClient(SecurityClientBase):
    def test_api(self):
        api_call = ConfigApi.test_api()
        sdk_request = SdkRequestBuilder.build_sdk_request(api_call)
        return self.make_request(sdk_request)


class NlpClient(SecurityClientBase):
    def save_dataset(self, dataset_id, generator):
        api_call = NlpApi.save_dataset_api(dataset_id, generator)
        sdk_request = SdkRequestBuilder.build_sdk_request(api_call)
        return self.make_request(sdk_request)



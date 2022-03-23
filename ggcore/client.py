"""Define client related classes for the sdk."""

import typing

from ggcore.api import SecurityApi, SdkRequestBuilder, NlpApi, ConfigApi
from ggcore.config import SdkBootstrapConfig, SdkSecurityConfig
from ggcore.http_base import SdkHttpClient
from ggcore.sdk_messages import SdkServiceResponse, SdkServiceRequest
from ggcore.security_base import SdkAuthHeaderBuilder
from ggcore.session import TokenFactory


# pylint: disable=too-few-public-methods
class ClientBase:
    """Define base class for the other clients."""
    _bootstrap_config: SdkBootstrapConfig

    def __init__(self, bootstrap_config):
        self._bootstrap_config = bootstrap_config

    def make_request(self,
                     sdk_request: SdkServiceRequest) -> SdkServiceResponse:
        """Define base make_request that all client calls pass through.
        Constructs sdk request url then invokes the request.
        """
        # set sdk request url
        sdk_request.url = f'http://{self._bootstrap_config.url_base}/1.0/{sdk_request.api_endpoint}'

        # invoke request
        return SdkHttpClient.invoke(sdk_request)


class SecurityClient(ClientBase):
    """Define Security client for bootstrapping the sdk. Makes http requests
    to the SecurityModule. Stores state of the current SdkSecurityConfig (
    includes token).
    """
    _security_config: SdkSecurityConfig

    def __init__(self, bootstrap_config):
        super().__init__(bootstrap_config)
        self._security_config = SdkSecurityConfig(bootstrap_config)

    def request_and_store_token(self):
        """Build and execute request to get the security token, store the
        token result.
        """
        sdk_request = SdkRequestBuilder.build_partial_sdk_request(
            SecurityApi.get_token_api())

        auth_basic_header = SdkAuthHeaderBuilder.get_basic_header(
            self._security_config)
        sdk_request.headers.update(auth_basic_header)

        token = self.make_request(sdk_request)

        self._security_config.token = token

        return token

    def is_token_present(self):
        """Return true if token is present with the security config."""
        return bool(self._security_config.token)

    # pylint: disable=missing-function-docstring
    @property
    def security_config(self):
        return self._security_config


class SecurityClientBase(ClientBase):
    """Define Security client base. Provide authentication headers to client
    subclasses. Instantiates TokenFactory for get token calls.
    """
    _security_client: SecurityClient
    _token_factory: TokenFactory

    def __init__(self, bootstrap_config):
        super().__init__(bootstrap_config)

        # Configure security client and token factory
        self._security_client = SecurityClient(self._bootstrap_config)
        self._token_factory = TokenFactory(
            self._security_client.request_and_store_token)

    def make_request(self,
                     sdk_request: SdkServiceRequest) -> SdkServiceResponse:
        """Define make_request that adds bearer auth headers for the sdk
        request.
        """
        # todo Add support for getting new token when the present one expires
        # very basic token management, gets token once then uses that
        if not self._security_client.is_token_present():
            # token not present, so get and store it
            self._token_factory.get_token_from_request()

        # add token header to request
        sdk_request.add_headers(SdkAuthHeaderBuilder.get_bearer_header(
            self._security_client.security_config))

        return super().make_request(sdk_request)


class ConfigClient(SecurityClientBase):
    """Define ConfigClient to hold the config sdk calls."""

    def test_api(self):
        """Return test api sdk call."""
        api_call = ConfigApi.test_api()
        sdk_request = SdkRequestBuilder.build_partial_sdk_request(api_call)
        return self.make_request(sdk_request)

    def get_data(self, module: str,
                 profiles: typing.Union[str, typing.List[str]],
                 revision: str):
        """Return get data sdk call."""
        api_call = ConfigApi.get_data_api(module, profiles, revision)
        sdk_request = SdkRequestBuilder.build_partial_sdk_request(api_call)
        return self.make_request(sdk_request)


class NlpClient(SecurityClientBase):
    """Define NlpClient to hold the nlp sdk calls."""

    def save_dataset(self, generator: typing.Generator, dataset_id: str,
                     overwrite: bool):
        """Return save dataset sdk call."""
        api_call = NlpApi.save_dataset_api(generator, dataset_id, overwrite)
        sdk_request = SdkRequestBuilder.build_partial_sdk_request(api_call)
        return self.make_request(sdk_request)

"""Define client related classes for the sdk."""

import typing

from ggcore.api import SecurityApi, SdkRequestBuilder, NlpApi, ConfigApi, \
    AbstractApi
from ggcore.config import SdkBootstrapConfig, SdkSecurityConfig
from ggcore.http_base import SdkHttpClient
from ggcore.sdk_messages import SdkServiceRequest, \
    SdkResponseHelper, CheckTokenResponse
from ggcore.security_base import SdkAuthHeaderBuilder
from ggcore.session import TokenFactory
from ggcore.utils import DOCKER_NGINX_PORT


# pylint: disable=too-few-public-methods
class ClientBase:
    """Define base class for the other clients."""
    _bootstrap_config: SdkBootstrapConfig

    def __init__(self, bootstrap_config):
        self._bootstrap_config = bootstrap_config

    # pylint: disable=no-self-use
    def make_request(self,
                     sdk_request: SdkServiceRequest) -> SdkResponseHelper:
        """Define base make_request that all client calls pass through."""
        # invoke request
        return SdkHttpClient.invoke(sdk_request)

    def build_sdk_request(self,
                          api_def: AbstractApi) -> SdkServiceRequest:
        """Define base build_sdk_request that all client calls pass through.
        Sets the 'url' property of SdkServiceRequest based on bootstrap config.
        """
        sdk_request = SdkRequestBuilder.build_partial_sdk_request(api_def)

        if self._bootstrap_config.is_docker_context:
            # sdk running in docker context, set the host to be the same as
            # the api endpoint.
            sdk_request.url = f'http://{sdk_request.docker_base}' \
                              f':{DOCKER_NGINX_PORT}' \
                              f'/1.0/{sdk_request.api_endpoint}'
        else:
            # sdk running natively, set the host to be the static url base
            # passed in on init.
            sdk_request.url = f'http://{self._bootstrap_config.url_base}' \
                              f'/1.0/{sdk_request.api_endpoint}'

        return sdk_request


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
        sdk_request = self.build_sdk_request(
            SecurityApi.get_token_api())

        auth_basic_header = SdkAuthHeaderBuilder.get_basic_header(
            self._security_config)
        sdk_request.headers.update(auth_basic_header)

        sdk_response_helper = self.make_request(sdk_request)

        return sdk_request.api_response_handler(sdk_response_helper)

    def is_token_present(self):
        """Return true if token is present with the security config."""
        return bool(self._security_config.token)

    def check_token_builtin(self) -> CheckTokenResponse:
        """Define method that runs a check token call."""
        sdk_request = self.build_sdk_request(
            SecurityApi.check_token_api(self.security_config.token))

        auth_basic_header = SdkAuthHeaderBuilder.get_basic_header(
            self._security_config)

        sdk_request.headers.update(auth_basic_header)

        sdk_response_helper = self.make_request(sdk_request)

        return sdk_request.api_response_handler(sdk_response_helper)

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

    def build_sdk_request(self,
                          api_def: AbstractApi) -> SdkServiceRequest:
        sdk_request = super().build_sdk_request(api_def)

        # token handling
        token_tracker = self._token_factory.token_handling()

        self._security_client.security_config.token = token_tracker.token

        sdk_request.add_headers(SdkAuthHeaderBuilder.get_bearer_header(
            self._security_client.security_config))

        return sdk_request

    def call_api(self, api: AbstractApi):
        """Define method that builds and makes SDK requests from an API
        definition.
        """
        sdk_request = self.build_sdk_request(api)
        sdk_response_helper = self.make_request(sdk_request)

        # if the request returns a 401 Unauthorized then check token
        # and possibly retry
        if sdk_response_helper.status_code == 401:
            # request hit a 401, call check token
            check_token_response = self._security_client.check_token_builtin()

            # token is valid, surface issue
            if check_token_response.status_code == 200:
                raise RuntimeError(
                    f"Error: Request returned a '401 Unauthorized' but "
                    f"check_token confirmed a valid token is being used. "
                    f"Original response error '"
                    f"{sdk_response_helper.response}'.")

            # token is invalid, get token again and retry
            if check_token_response.status_code == 400:
                # call for a new token
                self._token_factory.call_for_token()

                # build new sdk request and make new request
                sdk_request = self.build_sdk_request(api)
                sdk_response_helper = self.make_request(sdk_request)

        # custom handler call if response passes generic checks
        return sdk_request.api_response_handler(sdk_response_helper)


class ConfigClient(SecurityClientBase):
    """Define ConfigClient to hold the config sdk calls."""

    def test_api(self, test_message: str):
        """Return test api sdk call."""
        api_call = ConfigApi.test_api(test_message)
        return self.call_api(api_call)

    def get_data(self, module: str,
                 profiles: typing.Union[str, typing.List[str]],
                 revision: str):
        """Return get data sdk call."""
        api_call = ConfigApi.get_data_api(module, profiles, revision)
        return self.call_api(api_call)


class NlpClient(SecurityClientBase):
    """Define NlpClient to hold the nlp sdk calls."""

    def save_dataset(self, generator: typing.Generator, dataset_id: str,
                     overwrite: bool):
        """Return save dataset sdk call."""
        api_call = NlpApi.save_dataset_api(generator, dataset_id, overwrite)
        return self.call_api(api_call)

    def promote_model(self, model_name: str, nlp_task: str, environment: str):
        """Return promote model sdk call."""
        api_call = NlpApi.promote_model_api(model_name, nlp_task, environment)
        return self.call_api(api_call)

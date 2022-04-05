"""Define client related classes for the sdk."""

import typing

from ggcore.api import SecurityApi, SdkRequestBuilder, NlpApi, ConfigApi, \
    AbstractApi
from ggcore.config import SdkBootstrapConfig, SdkSecurityConfig
from ggcore.http_base import SdkHttpClient
from ggcore.sdk_exceptions import SdkUnauthorizedValidTokenException, \
    SdkUnauthorizedInvalidTokenException
from ggcore.sdk_messages import SdkServiceRequest, \
    SdkResponseHelper, CheckTokenResponse, GetTokenResponse
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
        return SdkHttpClient.execute_request(sdk_request)

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
    _token_factory: TokenFactory

    def __init__(self, bootstrap_config):
        super().__init__(bootstrap_config)
        self._security_config = SdkSecurityConfig(bootstrap_config)
        self._token_factory = TokenFactory(
            self.get_token_builtin)

    def get_token_builtin(self) -> GetTokenResponse:
        """Build and execute request to get a new security token."""
        # get api
        api = SecurityApi.get_token_api()

        # build request
        sdk_request = self.build_sdk_request(api)

        # invoke request
        sdk_response_helper = self._invoke_with_basic_auth(sdk_request)

        # handle and return
        return api.handler(sdk_response_helper)

    def check_token_builtin(self) -> CheckTokenResponse:
        """Build and execute request to check the current security token."""
        # get api
        api = \
            SecurityApi.check_token_api(self._token_factory.get_current_token())

        # build request
        sdk_request = self.build_sdk_request(api)

        # invoke request
        sdk_response_helper = self._invoke_with_basic_auth(sdk_request)

        # handle and return
        return api.handler(sdk_response_helper)

    def _invoke_with_basic_auth(self, sdk_request):
        """Define method to invoke sdk requests with basic auth headers and
        return the handled response.
        """
        auth_basic_header = SdkAuthHeaderBuilder.get_basic_header(
            self._security_config)

        sdk_request.headers.update(auth_basic_header)

        return self.make_request(sdk_request)

    def prepare_auth(self, force_token_refresh=False):
        self._token_factory.refresh_token(force_token_refresh)

    def authenticate_request(self, sdk_request: SdkServiceRequest):
        sdk_request.add_headers(
            SdkAuthHeaderBuilder.get_bearer_header_for_token(
                self._token_factory.get_current_token()))
        return sdk_request


class SecurityClientBase(ClientBase):
    """Define Security client base. Provide authentication and response
    handling logic to client subclasses.
    """
    _security_client: SecurityClient

    def __init__(self, bootstrap_config):
        super().__init__(bootstrap_config)

        # Configure security client
        self._security_client = SecurityClient(self._bootstrap_config)

    def build_sdk_request(self,
                          api_def: AbstractApi) -> SdkServiceRequest:
        # call superclass build_sdk_request
        sdk_request = super().build_sdk_request(api_def)

        # authenticate request
        self._security_client.authenticate_request(sdk_request)

        return sdk_request

    def call_api(self, api: AbstractApi,
                 force_token_refresh=False) -> SdkResponseHelper:
        """Define method that composes the steps for a full api call."""
        # prepare auth for call
        self._security_client.prepare_auth(force_token_refresh)

        # build request
        sdk_request = self.build_sdk_request(api)

        # make request
        return self.make_request(sdk_request)

    def generic_response_handler(self, sdk_response_helper: SdkResponseHelper):
        """Define method for generically processing responses before being
        passed to specific api handlers.
        """
        # if the request returns a 401 Unauthorized then check token
        # and possibly retry
        if sdk_response_helper.status_code == 401:
            # request hit a 401, call check token
            check_token_response = self._security_client.check_token_builtin()

            # token is valid, surface unrecoverable exception
            if check_token_response.status_code == 200:
                raise SdkUnauthorizedValidTokenException(
                    sdk_response_helper.response)

            # token is invalid, surface recoverable exception
            if check_token_response.status_code == 400:
                raise SdkUnauthorizedInvalidTokenException()

    def invoke(self, api: AbstractApi):
        """Define method that builds and makes SDK requests from an API
        definition.
        """
        sdk_response_helper = self.call_api(api)

        try:
            self.generic_response_handler(sdk_response_helper)
        except SdkUnauthorizedInvalidTokenException:
            # single retry for invalid token
            sdk_response_helper = self.call_api(api, force_token_refresh=True)

        # custom handler call if response passes generic handler
        return api.handler(sdk_response_helper)


class ConfigClient(SecurityClientBase):
    """Define ConfigClient to hold the config sdk calls."""

    def test_api(self, test_message: str):
        """Return test api sdk call."""
        api_call = ConfigApi.test_api(test_message)
        return self.invoke(api_call)

    def get_data(self, module: str,
                 profiles: typing.Union[str, typing.List[str]],
                 revision: str):
        """Return get data sdk call."""
        api_call = ConfigApi.get_data_api(module, profiles, revision)
        return self.invoke(api_call)


class NlpClient(SecurityClientBase):
    """Define NlpClient to hold the nlp sdk calls."""

    def save_dataset(self, generator: typing.Generator, dataset_id: str,
                     overwrite: bool):
        """Return save dataset sdk call."""
        api_call = NlpApi.save_dataset_api(generator, dataset_id, overwrite)
        return self.invoke(api_call)

    def promote_model(self, model_name: str, nlp_task: str, environment: str):
        """Return promote model sdk call."""
        api_call = NlpApi.promote_model_api(model_name, nlp_task, environment)
        return self.invoke(api_call)

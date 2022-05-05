"""Define client related classes for the sdk."""

import typing

from graphgrid_sdk.ggcore.api import SecurityApi, SdkRequestBuilder, NlpApi, \
    ConfigApi, AbstractApi
from graphgrid_sdk.ggcore.config import SdkBootstrapConfig
from graphgrid_sdk.ggcore.http_base import SdkHttpClient
from graphgrid_sdk.ggcore.sdk_exceptions import \
    SdkUnauthorizedValidTokenException, SdkUnauthorizedInvalidTokenException
from graphgrid_sdk.ggcore.sdk_messages import SdkServiceRequest, \
    GetTokenResponse, CheckTokenResponse, GenericResponse, PromoteModelResponse, \
    SaveDatasetResponse, GetDataResponse, DagRunResponse, \
    NMTStatusResponse, NMTTrainResponse, TrainRequestBody
from graphgrid_sdk.ggcore.security_base import SdkAuthHeaderBuilder
from graphgrid_sdk.ggcore.session import TokenFactory
from graphgrid_sdk.ggcore.utils import DOCKER_NGINX_PORT


# pylint: disable=too-few-public-methods
class ClientBase:
    """Define base class for the other clients."""
    _bootstrap_config: SdkBootstrapConfig

    def __init__(self, bootstrap_config):
        self._bootstrap_config = bootstrap_config

    # pylint: disable=no-self-use
    def make_request(self,
                     sdk_request: SdkServiceRequest) -> GenericResponse:
        """Define base make_request that all client calls pass through.
        Return the resulting generic response.
        """
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


class InternalSecurityClient(ClientBase):
    """Define internal security client for bootstrapping the sdk. Special
    client that supports token operations and provides auth to sdk requests.

    Defines protected methods for get token and check token, which are used
    by the TokenFactory.

    Meant for internal sdk core use only. User-facing security SDK calls
    should go in SecurityClient instead.
    """
    _token_factory: TokenFactory

    def __init__(self, bootstrap_config):
        super().__init__(bootstrap_config)
        self._token_factory = TokenFactory(
            self._get_token_builtin, self._check_token_builtin)

    def _get_token_builtin(self) -> GetTokenResponse:
        """Define protected method to get a new security token."""
        api = SecurityApi.get_token_api()

        # invoke request
        return self._invoke_with_basic_auth(api)

    def _check_token_builtin(self) -> CheckTokenResponse:
        """Define protected method to check the current security token."""
        api = \
            SecurityApi.check_token_api(self._token_factory.get_current_token())

        # invoke request
        return self._invoke_with_basic_auth(api)

    def _invoke_with_basic_auth(self, api: AbstractApi):
        """Define protected method to invoke sdk requests with basic auth
        headers and return the handled response.
        """
        # build request
        sdk_request = self.build_sdk_request(api)

        # apply basic auth header
        auth_basic_header = SdkAuthHeaderBuilder.get_basic_header(
            self._bootstrap_config)
        sdk_request.headers.update(auth_basic_header)

        generic_response = self.make_request(sdk_request)

        return api.handler(generic_response)

    def prepare_auth(self, force_token_refresh=False):
        """Define method that prepares token factory for use."""
        self._token_factory.refresh_token(force_token_refresh)

    def check_token(self) -> CheckTokenResponse:
        """Define method that checks the current token and returns the
        response.
        """
        return self._token_factory.call_check_token()

    def authenticate_request(self, sdk_request: SdkServiceRequest):
        """Define method that adds the current token as a bearer header to
        the sdk request.
        """
        sdk_request.add_headers(
            SdkAuthHeaderBuilder.get_bearer_header(
                self._token_factory.get_current_token()))
        return sdk_request


class SecurityClientBase(ClientBase):
    """Define Security client base. Provide authentication and response
    handling logic to client subclasses.
    """
    _security_client: InternalSecurityClient

    def __init__(self, bootstrap_config):
        super().__init__(bootstrap_config)

        # Configure security client
        self._security_client = InternalSecurityClient(self._bootstrap_config)

    def build_sdk_request(self,
                          api_def: AbstractApi) -> SdkServiceRequest:
        # call superclass build_sdk_request
        sdk_request = super().build_sdk_request(api_def)

        # authenticate request
        self._security_client.authenticate_request(sdk_request)

        return sdk_request

    def call_api(self, api: AbstractApi,
                 force_token_refresh=False) -> GenericResponse:
        """Define method that composes the steps for a full api call."""
        # prepare auth for call
        self._security_client.prepare_auth(force_token_refresh)

        # build request
        sdk_request = self.build_sdk_request(api)

        # make request
        return self.make_request(sdk_request)

    def generic_response_handler(self, generic_response: GenericResponse):
        """Define method for generically processing responses before being
        passed to specific api handlers.
        """
        # if the request returns a 401 Unauthorized then check token
        # and possibly retry
        if generic_response.status_code == 401:
            # request hit a 401, call check token
            check_token_response = self._security_client.check_token()

            # token is valid, surface unrecoverable exception
            if check_token_response.status_code == 200:
                raise SdkUnauthorizedValidTokenException(
                    generic_response.response)

            # token is invalid, surface recoverable exception
            if check_token_response.status_code == 400:
                raise SdkUnauthorizedInvalidTokenException()

    def invoke(self, api: AbstractApi):
        """Define method that builds and makes SDK requests from an API
        definition.
        """
        generic_response = self.call_api(api)

        try:
            self.generic_response_handler(generic_response)
        except SdkUnauthorizedInvalidTokenException:
            # single retry for invalid token
            generic_response = self.call_api(api, force_token_refresh=True)

        # custom handler call if response passes generic handler
        return api.handler(generic_response)


class SecurityClient(SecurityClientBase):
    """Define SecurityClient to hold the security sdk calls."""


class ConfigClient(SecurityClientBase):
    """Define ConfigClient to hold the config sdk calls."""

    def test_api(self, test_message: str):
        """Return test api sdk call."""
        api_call = ConfigApi.test_api(test_message)
        return self.invoke(api_call)

    def get_data(self, module: str,
                 profiles: typing.Union[str, typing.List[str]],
                 revision: str) -> GetDataResponse:
        """Return get data sdk call."""
        api_call = ConfigApi.get_data_api(module, profiles, revision)
        return self.invoke(api_call)


class NlpClient(SecurityClientBase):
    """Define NlpClient to hold the nlp sdk calls."""

    def save_dataset(self, generator: typing.Generator, dataset_id: str,
                     overwrite: bool) -> SaveDatasetResponse:
        """Return save dataset sdk call."""
        api_call = NlpApi.save_dataset_api(generator, dataset_id, overwrite)
        return self.invoke(api_call)

    def promote_model(self, model_name: str, nlp_task: str,
                      environment: str) -> PromoteModelResponse:
        """Return promote model sdk call."""
        api_call = NlpApi.promote_model_api(model_name, nlp_task, environment)
        return self.invoke(api_call)

    def get_dag_run_status(self, dag_id: str,
                           dag_run_id: str) -> DagRunResponse:
        """Return get dag run status sdk call."""
        api_call = NlpApi.get_dag_run_status_api(dag_id, dag_run_id)
        return self.invoke(api_call)

    def trigger_dag(self, dag_id: str, request_body: dict) -> DagRunResponse:
        """Return trigger dag sdk call."""
        api_call = NlpApi.trigger_dag_api(dag_id, request_body)
        return self.invoke(api_call)

    def get_nmt_status(self, dag_run_id: str) -> NMTStatusResponse:
        """Return nmt train status call."""
        api_call = NlpApi.nmt_status_api(dag_run_id)
        return self.invoke(api_call)

    def trigger_nmt(self, request_body: TrainRequestBody) -> NMTTrainResponse:
        """Return job train sdk call."""
        api_call = NlpApi.nmt_train_api(request_body)
        return self.invoke(api_call)

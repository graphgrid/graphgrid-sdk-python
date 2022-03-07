import requests

from ggcore.client import AbstractApi
from ggcore.sdk_messages import SdkServiceRequest
from ggcore.sdk_messages import SdkServiceResponse
from ggcore.security_base import SdkAuth
from ggcore.utils import HttpMethod, RequestAuthType


def http_response_to_sdk_response(http_response: requests.Response):
    sdk_response = SdkServiceResponse()

    sdk_response.statusCode = http_response.status_code

    sdk_response.response = http_response.content.decode()

    try:
        http_response.raise_for_status()
    except requests.HTTPError as e:
        sdk_response.exception = e

    sdk_response.statusText = http_response.reason
    return sdk_response


def execute_request(sdk_request: SdkServiceRequest, method: HttpMethod) -> SdkServiceResponse:
    http_response: requests.Response = requests.request(method=method.value,
                                                        url=sdk_request.endpoint,
                                                        params=sdk_request.query_params,
                                                        data=sdk_request.body,
                                                        headers=sdk_request.headers)

    sdk_response: SdkServiceResponse = http_response_to_sdk_response(http_response)
    return sdk_response


class SdkHttpBase:

    # should pass in credentials obj or session obj?
    # todo think this is still needed, but unsure of where it lives/how it gets auth/if the new session covers this
    def create_sdk_service_request_from_api_request_and_session(self, aa: AbstractApi,) -> SdkServiceRequest:
        sdk_req = SdkServiceRequest() # will this result in error?

        headers = dict

        sdk_auth = SdkAuth(credentials=None)

        # Set Auth Type
        if aa.auth_type() == RequestAuthType.BASIC:
            sdk_req.request_auth_method = RequestAuthType.BASIC
            headers.update(sdk_auth.get_auth_for_http(auth_type=RequestAuthType.BASIC))

        elif aa.auth_type() == RequestAuthType.BEARER:
            sdk_req.request_auth_method = RequestAuthType.BEARER
            headers.update(sdk_auth.get_auth_for_http(auth_type=RequestAuthType.BEARER))

        # Set custom api headers?
            # todo custom api related headers set here? Is that something we actually need (YNGNI?)
            #   Will a way to construct custom headers based on the api call be needed?
            #    Will it need to be a mix of static api info and session/config info, or can we just get away with static api header info?



        return sdk_req





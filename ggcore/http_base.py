import requests

from ggcore.sdk_messages import SdkServiceRequest
from ggcore.sdk_messages import SdkServiceResponse


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


def execute_request(sdk_request: SdkServiceRequest,) -> SdkServiceResponse:
    http_response: requests.Response = requests.request(method=sdk_request.http_method.value,
                                                        url=sdk_request.endpoint,
                                                        params=sdk_request.query_params,
                                                        data=sdk_request.body,
                                                        headers=sdk_request.headers)

    sdk_response: SdkServiceResponse = http_response_to_sdk_response(http_response)
    return sdk_response

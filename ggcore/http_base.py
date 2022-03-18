"""Define classes for building, executing, processing http requests."""
import requests

from ggcore.sdk_messages import SdkServiceRequest
from ggcore.sdk_messages import SdkServiceResponse


class SdkHttpClient:
    """Define class containing all sdk http methods."""

    @classmethod
    def http_response_to_sdk_response(cls, http_response: requests.Response):
        """Build an SdkServiceResponse from the http response."""
        sdk_response = SdkServiceResponse()

        sdk_response.status_code = http_response.status_code

        # todo will need to map response body to specific response-type objs
        sdk_response.response = http_response.content.decode()

        try:
            http_response.raise_for_status()
        except requests.RequestException as request_exception:
            sdk_response.exception = request_exception

        sdk_response.status_text = http_response.reason
        return sdk_response

    @classmethod
    def execute_request(cls,
                        sdk_request: SdkServiceRequest) -> SdkServiceResponse:
        """Build and execute http request."""
        http_response: requests.Response = requests.request(
            method=sdk_request.http_method.value,
            url=sdk_request.url,
            params=sdk_request.query_params,
            data=sdk_request.body,
            headers=sdk_request.headers)

        sdk_response: SdkServiceResponse = cls.http_response_to_sdk_response(
            http_response)
        return sdk_response

    @classmethod
    def invoke(cls, sdk_request: SdkServiceRequest):
        """Invoke the sdk request: execute the corresponding http request
        and processing the response.
        """
        sdk_response = cls.execute_request(sdk_request)
        return sdk_request.api_response_handler(sdk_response)

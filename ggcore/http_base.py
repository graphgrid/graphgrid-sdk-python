"""Define classes for building, executing, processing http requests."""
import requests

from ggcore.sdk_messages import SdkServiceRequest, SdkResponseHelper


class SdkHttpClient:
    """Define class containing all sdk http methods."""

    @classmethod
    def http_response_to_sdk_response(cls, http_response: requests.Response):
        """Build an SdkServiceResponse from the http response."""
        sdk_response = SdkResponseHelper()

        sdk_response.status_code = http_response.status_code
        sdk_response.status_text = http_response.reason
        sdk_response.response = http_response.content.decode()

        try:
            # raise exception if one occurred
            http_response.raise_for_status()

            # otherwise, set exception to None
            sdk_response.exception = None
        except requests.RequestException as request_exception:
            sdk_response.exception = request_exception

        return sdk_response

    @classmethod
    def execute_request(cls,
                       sdk_request: SdkServiceRequest) -> SdkResponseHelper:
        """Invoke the SdkServiceRequest by building and executing an http
        request.
        """
        http_response: requests.Response = requests.request(
            method=sdk_request.http_method.value,
            url=sdk_request.url,
            params=sdk_request.query_params,
            data=sdk_request.body,
            headers=sdk_request.headers)

        sdk_response: SdkResponseHelper = cls.http_response_to_sdk_response(
            http_response)
        return sdk_response

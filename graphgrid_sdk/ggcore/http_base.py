"""Define classes for building, executing, processing http requests."""
import requests

from graphgrid_sdk.ggcore.sdk_messages import SdkServiceRequest, GenericResponse


class SdkHttpClient:
    """Define class containing all sdk http methods."""

    @classmethod
    def http_response_to_generic_response(cls,
                                          http_response: requests.Response):
        """Build a GenericResponse from the http response."""
        generic_response = GenericResponse()

        generic_response.status_code = http_response.status_code
        generic_response.status_text = http_response.reason
        generic_response.response = http_response.content.decode()

        try:
            # raise exception if one occurred
            http_response.raise_for_status()

            # otherwise, set exception to None
            generic_response.exception = None
        except requests.RequestException as request_exception:
            generic_response.exception = request_exception

        return generic_response

    @classmethod
    def execute_request(cls,
                        sdk_request: SdkServiceRequest) -> GenericResponse:
        """Invoke the SdkServiceRequest by building and executing an http
        request.
        """
        http_response: requests.Response = requests.request(
            method=sdk_request.http_method.value,
            url=sdk_request.url,
            params=sdk_request.query_params,
            data=sdk_request.body,
            headers=sdk_request.headers)

        return cls.http_response_to_generic_response(http_response)

import requests

from ggcore.sdk_messages import SdkServiceRequest
from ggcore.sdk_messages import SdkServiceResponse


class SdkHttpClient:
    @classmethod
    def http_response_to_sdk_response(cls, http_response: requests.Response):
        sdk_response = SdkServiceResponse()

        sdk_response.statusCode = http_response.status_code

        # todo will need to map response body to specific response-type objs
        sdk_response.response = http_response.content.decode()

        try:
            http_response.raise_for_status()
        except requests.RequestException as e:
            sdk_response.exception = e

        sdk_response.statusText = http_response.reason
        return sdk_response

    @classmethod
    def execute_request(cls,
                        sdk_request: SdkServiceRequest, ) -> SdkServiceResponse:
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
        sdk_response = cls.execute_request(sdk_request)
        return sdk_request.api_response_handler(sdk_response)

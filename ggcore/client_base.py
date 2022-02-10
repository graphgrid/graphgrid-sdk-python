import typing
from _typeshed import SupportsRead

import requests
import json
from ggcore.sdk_messages import SdkServiceRequest

from ggcore import utils
from ggcore.sdk_messages import SdkServiceResponse
from ggcore.utils import HttpMethod


class SdkClientBase:

    def execute_request(self, sdk_request: SdkServiceRequest, method: HttpMethod) -> SdkServiceResponse:
        http_response: requests.Response = requests.request(method=method.value,
                                                            url=sdk_request.endpoint,
                                                            params=sdk_request.query_params,
                                                            data=sdk_request.body,
                                                            headers=sdk_request.headers)

        sdk_response: SdkServiceResponse = utils.http_response_to_sdk_response(http_response)
        return sdk_response

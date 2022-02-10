import typing

import urllib
from dataclasses import dataclass


@dataclass
class SdkServiceRequest:
    endpoint: str
    # serviceUrl: str # see java sdk analog; used internally?

    # request_handler: object
    # response_handler: object
    request_auth_method: object

    headers: dict = None
    query_params: dict = None
    body: dict = None


@dataclass
class SdkServiceResponse:
    statusCode: int
    statusText: str

    response: object = dict({})
    exception: Exception = None


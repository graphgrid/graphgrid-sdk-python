import dataclasses
from dataclasses import dataclass

from ggcore.utils import RequestAuthType


@dataclass
class SdkServiceRequest:
    endpoint: str
    # serviceUrl: str # see java sdk analog; used internally?

    # request_handler: object
    # response_handler: object
    request_auth_method: RequestAuthType

    headers: dict = dataclasses.field(default_factory=dict)
    query_params: dict = dataclasses.field(default_factory=dict)
    body: dict = dataclasses.field(default_factory=dict)


@dataclass
class SdkServiceResponse:
    statusCode: int = None
    statusText: str = None

    response: dict = dataclasses.field(default_factory=dict)
    exception: Exception = None

import enum
import json

import requests

from ggcore.sdk_messages import SdkServiceResponse

POST = "post"
GET = "get"
PUT = "put"
DELETE = "delete"
PATCH = "patch"
OPTIONS = "options"
CONNECT = "connect"
HEAD = "head"
TRACE = "trace"


class HttpMethod(enum.Enum):
    post = POST
    get = GET
    put = PUT
    delete = DELETE
    patch = PATCH
    options = OPTIONS
    connect = CONNECT
    head = HEAD
    trace = TRACE


def http_response_to_sdk_response(http_response: requests.Response):
    sdk_response = SdkServiceResponse()

    sdk_response.statusCode = http_response.status_code
    sdk_response.response = json.load(http_response.content)

    try:
        http_response.raise_for_status()
    except requests.HTTPError as e:
        sdk_response.exception = e

    sdk_response.statusText = http_response.reason


CONFIG = 'config'
SECURITY = 'security'
NLP = 'nlp'

SUPPORTED_CLIENTS = [CONFIG, SECURITY]
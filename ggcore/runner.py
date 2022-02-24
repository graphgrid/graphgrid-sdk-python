from ggcore.client import ApiRequest
from ggcore.session import SessionCore


def call_api(api_request: ApiRequest, session: SessionCore):
    """
    missing items:
        - client_name for http
    """
    api_request.endpoint()
from ggcore.client import AbstractApi
from ggcore.session import SessionCore


def call_api(api_request: AbstractApi, session: SessionCore):
    """
    missing items:
        - client_name for http
    """
    api_request.endpoint()
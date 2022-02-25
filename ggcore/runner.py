from ggcore.client import AbstractApi
from ggcore.config import URL_BASE
from ggcore.session import SessionCore


def call_api(api_request: AbstractApi, session: SessionCore):
    """
    missing items:
        - client_name for http
    """

    url_base = session.get_config(URL_BASE)
    client_name = api_request.client_name()
    endpoint = api_request.endpoint()

    http_request = f'http://{url_base}/1.0/{client_name}/{endpoint}'

    # build http request (obj)




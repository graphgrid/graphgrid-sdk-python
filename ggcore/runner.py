from ggcore import http_base
from ggcore.client import AbstractApi
from ggcore.config import URL_BASE
from ggcore.sdk_messages import SdkServiceRequest, SdkServiceResponse
from ggcore.security_base import SdkAuth
from ggcore.session import SessionCore
from ggcore.utils import GRANT_TYPE_KEY, GRANT_TYPE_CLIENT_CREDENTIALS


# def call_api(api_request: AbstractApi, session: SessionCore):
#     """
#     missing items:
#         - client_name for http
#
#
#     can some of the duplication in this be removed? like we have to reference the auth type twice and http method type twice,
#         can these be defined once with better/cleaner classes?
#     """
#
#     url_base = session.get_config(URL_BASE)
#     client_name = api_request.client_name()
#     endpoint = api_request.endpoint()
#
#     api_uri = f'http://{url_base}/1.0/{client_name}/{endpoint}'
#
#     auth_header = SdkAuth(credentials=session.credentials).get_auth_for_http(auth_type=api_request.auth_type())
#
#     sdk_request = SdkServiceRequest(endpoint=api_uri,
#                                     request_auth_method=api_request.auth_type(),
#                                     headers=auth_header,
#                                     query_params=api_request.query_params())
#
#     # Execute Request
#     sdk_response: SdkServiceResponse = http_base.execute_request(sdk_request, api_request.http_method())
#
#     # Handle response
#     return api_request.handler(sdk_response)
#
#
#


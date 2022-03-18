"""Define util constants and enums."""

import enum

# GG MODULE CLIENTS
CONFIG = 'config'
SECURITY = 'security'
NLP = 'nlp'

SUPPORTED_CLIENTS = [CONFIG, SECURITY, NLP, ]

# HTTP METHODS
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
    """Define HTTP methods."""
    POST = POST
    GET = GET
    PUT = PUT
    DELETE = DELETE
    PATCH = PATCH
    OPTIONS = OPTIONS
    CONNECT = CONNECT
    HEAD = HEAD
    TRACE = TRACE


# SECURITY
AUTH_HEADER_KEY = "Authorization"
BASIC_HEADER_KEY = "Basic"
BEARER_HEADER_KEY = "Bearer"
GRANT_TYPE_KEY = "grant_type"
GRANT_TYPE_CLIENT_CREDENTIALS = "client_credentials"
PASSWORD_KEY = "password"
USERNAME_KEY = "username"

USER_AGENT = "User-Agent"
CONTENT_TYPE_HEADER_KEY = "Content-type"
CONTENT_TYPE_APP_JSON = "application/json"


class RequestAuthType(enum.Enum):
    """Define auth type keys."""
    BASIC = BASIC_HEADER_KEY
    BEARER = BEARER_HEADER_KEY

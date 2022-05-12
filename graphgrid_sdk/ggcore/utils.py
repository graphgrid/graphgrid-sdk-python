"""Define util constants and enums."""

import enum

# GG MODULE CLIENTS
CONFIG = 'config'
SECURITY = 'security'
NLP = 'nlp'

SUPPORTED_CLIENTS = [CONFIG, SECURITY, NLP, ]

DOCKER_NGINX_PORT = 8080

# HTTP METHODS
POST = "POST"
GET = "GET"
PUT = "PUT"
DELETE = "DELETE"
PATCH = "PATCH"
OPTIONS = "OPTIONS"
CONNECT = "CONNECT"
HEAD = "HEAD"
TRACE = "TRACE"


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
CONTENT_TYPE_APP_X_WWW_FORM_URLENCODED = "application/x-www-form-urlencoded"


class RequestAuthType(enum.Enum):
    """Define auth type keys."""
    BASIC = BASIC_HEADER_KEY
    BEARER = BEARER_HEADER_KEY


# CONFIG CONSTANTS
SPRING_OAUTH_CLIENT_ID = "spring.oauth.client.id"
SPRING_OAUTH_CLIENT_SECRET = "spring.oauth.client.secret"

# NLP / NMT Constants
NMT_DAG_ID = "nlp_model_training"

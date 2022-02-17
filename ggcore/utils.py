import enum

"""GG MODULE CLIENTS"""
CONFIG = 'config'
SECURITY = 'security'
NLP = 'nlp'

SUPPORTED_CLIENTS = [CONFIG, SECURITY, NLP, ]

"""HTTP METHODS"""
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


"""SECURITY"""
AUTH_HEADER_KEY = "Authorization"
BASIC_HEADER_KEY = "Basic"
BEARER_HEADER_KEY = "Bearer"
GRANT_TYPE_KEY = "grant_type"
PASSWORD_KEY = "password"
USERNAME_KEY = "username"


class RequestAuthType(enum.Enum):
    BASIC = BASIC_HEADER_KEY
    BEARER = BEARER_HEADER_KEY

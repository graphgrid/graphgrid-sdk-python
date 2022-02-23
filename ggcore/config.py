"""
configuration keys
"""

CLOUD_CONFIG_URI = "CLOUD_CONFIG_URI"
OAUTH_CLIENT_ID = "OAUTH_CLIENT_ID"
OAUTH_CLIENT_SECRET = "OAUTH_CLIENT_SECRET"
OAUTH_TOKEN_URL = "OAUTH_TOKEN_URL"

CONFIG_KEYS = {
    CLOUD_CONFIG_URI: "spring.cloud.config.uri",
    OAUTH_CLIENT_ID: "spring.oauth.client.id", # is this going to be retrieved from config or will the user pass this in manually by the Credentials?
    OAUTH_CLIENT_SECRET: "spring.oauth.client.secret",
    OAUTH_TOKEN_URL: "spring.oauth.tokenUrl", # default value is: http://security:8080/1.0/security/oauth/token, but wont we need it to be localhost for the sdk?
}

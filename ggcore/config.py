"""
configuration keys
"""

CLOUD_CONFIG_URI = "CLOUD_CONFIG_URI"
OAUTH_TOKEN_URL = "OAUTH_TOKEN_URL"




URL_BASE = "URL_BASE"                           # rename/revalue to API_BASE ?
OAUTH_CLIENT_ID = "OAUTH_CLIENT_ID"             # rename/revalue to ACCESS_KEY ?
OAUTH_CLIENT_SECRET = "OAUTH_CLIENT_SECRET"     # rename/revalue to SECRET_ACCESS_KEY ?

BOOTSTRAP_CONFIG_KEYS = [URL_BASE,
                         OAUTH_CLIENT_ID,
                         OAUTH_CLIENT_SECRET,]


# Other config
CONFIG_KEYS = {
    CLOUD_CONFIG_URI: "spring.cloud.config.uri",
    OAUTH_CLIENT_ID: "spring.oauth.client.id", # is this going to be retrieved from config or will the user pass this in manually by the Credentials?
    OAUTH_CLIENT_SECRET: "spring.oauth.client.secret",
    OAUTH_TOKEN_URL: "spring.oauth.tokenUrl", # default value is: http://security:8080/1.0/security/oauth/token, but wont we need it to be localhost for the sdk?
}


class SdkConfig(dict):

    # Method like these are for utility, to ensure we're always calling for the right config and also controlling what config gets exposed
    def url_base(self):
        return self.get(URL_BASE)

    def access_key(self):
        return self.get(OAUTH_CLIENT_ID)

    def secret_key(self):
        return self.get(OAUTH_CLIENT_SECRET)




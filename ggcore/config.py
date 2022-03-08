"""
configuration keys
"""

URL_BASE = "URL_BASE"                           # rename/revalue to SERVICE_BASE or API_BASE ?
OAUTH_CLIENT_ID = "OAUTH_CLIENT_ID"
OAUTH_CLIENT_SECRET = "OAUTH_CLIENT_SECRET"

BOOTSTRAP_CONFIG_KEYS = [URL_BASE,
                         OAUTH_CLIENT_ID,
                         OAUTH_CLIENT_SECRET,]


class SdkConfig(dict):

    # utility methods for specific config keys
    def url_base(self):
        return self.get(URL_BASE)

    def oauth_client_id(self):
        return self.get(OAUTH_CLIENT_ID)

    def oauth_client_secret(self):
        return self.get(OAUTH_CLIENT_SECRET)




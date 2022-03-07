from ggcore.config import SdkConfig, URL_BASE, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET
from ggcore.core import SdkCore

"""
example sdk usage?
    sdk = GraphGridSdk()
    
    sdk.save( "path/to/dataset" )
    
    sdk.
"""


class GraphGridSdk:
    """
    Class used to instantiate the GraphGridSdk
    """
    _core: SdkCore
    _config: SdkConfig = SdkConfig()

    # for now this works, but does it make more sense to setup a generic config map?
    def __init__(self, access_key, secret_access_key, url_base="localhost"):
        self._config[URL_BASE] = url_base
        self._config[OAUTH_CLIENT_ID] = access_key
        self._config[OAUTH_CLIENT_SECRET] = secret_access_key

        self._setup_core()

    # todo init so they can just pass in a config map instead of individual params like above?
    # def __init__(self, config: dict):
    #     self._config.update(config)
    #     self._setup_core()

    def _setup_core(self):
        self._core = SdkCore(self._config)


    def save_dataset(self):
        self._core.save_data()





import typing

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


    def experimental_get_token(self):
        pass

    # so for here its required to pass in a generator for streaming purposes, and then this passes to the base client for the body_fn, but
    #   this kinda begs the question of whether the requests should even be passing through the core, and instead maybe just call the clients directly themselves
    def save_dataset(self, dataset_id: str, generator: typing.Generator ):
        self._core.save_dataset(dataset_id, generator)





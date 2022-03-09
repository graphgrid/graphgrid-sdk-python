import typing

from ggcore.config import SdkBootstrapConfig
from ggcore.core import SdkCore


class GraphGridSdk:
    """
    GraphGridSdk is the user-facing resource to interact with GraphGrid modules
    """
    _core: SdkCore
    _config: SdkBootstrapConfig

    # todo init so they can just pass in a config map instead of individual params like above?
    def __init__(self, access_key, secret_access_key, url_base="localhost"):
        self._config = SdkBootstrapConfig(url_base, access_key, secret_access_key)
        self._setup_core()

    def _setup_core(self):
        self._core = SdkCore(self._config)

    def test_api(self):
        return self._core.test_api()

    def save_dataset(self, data_generator: typing.Generator, dataset_id: str = None, overwrite=False):
        self._core.save_dataset(data_generator, dataset_id, overwrite)

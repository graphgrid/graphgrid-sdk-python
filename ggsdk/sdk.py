import typing

from ggcore.config import SecurityConfig
from ggcore.core import SdkCore


class GraphGridSdk:
    """
    GraphGridSdk is the user-facing resource to interact with GraphGrid modules
    """
    _core: SdkCore
    _config: SecurityConfig

    def __init__(self, access_key, secret_access_key, url_base="localhost"):
        self._config = SecurityConfig(url_base, access_key, secret_access_key)
        self._setup_core()

    # todo init so they can just pass in a config map instead of individual params like above?
    # def __init__(self, config: dict):
    #     self._config.update(config)
    #     self._setup_core()

    def _setup_core(self):
        self._core = SdkCore(self._config)

    def test_api(self):
        return self._core.test_api()

    # todo dataset_id optional, overwrite added in (default false)
    def save_dataset(self, dataset_id: str, generator: typing.Generator):
        self._core.save_dataset(dataset_id, generator)

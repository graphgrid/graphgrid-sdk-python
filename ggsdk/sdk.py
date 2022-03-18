"""Define user-facing GraphGrid SDK."""
import typing

from ggcore.config import SdkBootstrapConfig
from ggcore.core import SdkCore


class GraphGridSdk:
    """Initialize the SDK Core for SDK calls. Expose those SDK calls as
    user-callable methods.
    """
    _core: SdkCore
    _config: SdkBootstrapConfig

    # todo init so they can just pass in a config map instead of individual
    #  params like above?
    def __init__(self, access_key, secret_access_key, url_base="localhost"):
        self._config = SdkBootstrapConfig(url_base, access_key,
                                          secret_access_key)
        self._setup_core()

    def _setup_core(self):
        self._core = SdkCore(self._config)

    def test_api(self):
        """Call test api."""
        return self._core.test_api()

    def save_dataset(self,
                     data_generator: typing.Generator,
                     dataset_id: str = None,
                     overwrite=False):
        """Call save dataset api.

        @param: data_generator  The generator providing dataset lines
        @param: dataset_id  Name/id for the dataset (default=None)
        @param: overwrite   Whether to overwrite the dataset if it already
            exists (default=False)
        """
        self._core.save_dataset(data_generator, dataset_id, overwrite)

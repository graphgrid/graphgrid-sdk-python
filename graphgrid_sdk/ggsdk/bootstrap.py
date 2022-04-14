"""Define methods for bootstrapping SDK config credentials."""
import os
import time

import javaproperties

from graphgrid_sdk.ggcore.config import SdkBootstrapConfig
from graphgrid_sdk.ggcore.utils import SPRING_OAUTH_CLIENT_ID, \
    SPRING_OAUTH_CLIENT_SECRET


def bootstrap_config_from_file():
    """Bootstrap SDK's configuration"""
    credentials_path = os.environ.get("GRAPHGRID_CONFIG_CREDENTIALS_PATH")
    credentials_filename = os.environ.get(
        "CONFIG_CREDENTIAL_PROPERTIES_FILENAME")
    credentials_full_path = os.path.join(credentials_path, credentials_filename)
    wait_for_file_creation(credentials_full_path)
    with open(credentials_full_path, "r") as file:
        config_dict = javaproperties.load(file)
        try:
            oauth_id = config_dict[SPRING_OAUTH_CLIENT_ID]
            oauth_secret = config_dict[SPRING_OAUTH_CLIENT_SECRET]

        except KeyError as error:
            raise RuntimeError(
                f"{credentials_full_path} did not contain the required key, "
                f"\"{error}\", to boostrap the SDK config.") from error

    # if autoconfig bootstrap running, it's in a docker context
    return SdkBootstrapConfig("localhost", oauth_id, oauth_secret, True)


def wait_for_file_creation(file_path: str, timeout: int = 30):
    """Wait for a file to be created"""
    timeout = time.time() + timeout
    while not os.path.exists(file_path):
        if time.time() > timeout:
            raise RuntimeError(f"Timed out waiting for {file_path}")
        time.sleep(5)

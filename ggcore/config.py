"""Define classes and constants for controlling sdk configuration."""

import typing
from dataclasses import dataclass


@dataclass
class SdkBootstrapConfig:
    """Define class representing bootstrap sdk configuration."""
    url_base: typing.AnyStr
    access_key: typing.AnyStr
    secret_key: typing.AnyStr
    is_docker_context: typing.Optional[bool]

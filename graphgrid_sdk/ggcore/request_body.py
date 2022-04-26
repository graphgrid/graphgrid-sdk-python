"""Define class for training request body."""

import json
from dataclasses import dataclass

import typing


@dataclass
class RequestBody:
    """Store Airflow configuration json/request bodies"""
    model: str
    datasets: typing.Union[dict, str]
    no_cache: bool = False
    GPU: bool = False

    def to_json(self):
        """Encode RequestBody to a json object"""
        return json.dumps(self.__dict__, indent=4)

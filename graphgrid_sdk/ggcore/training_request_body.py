"""Define class for training request body."""

import json
import typing
from dataclasses import dataclass

# pylint: disable=invalid-name
@dataclass
class TrainRequestBody:
    """Store Airflow configuration json/request bodies"""
    model: str
    datasets: typing.Union[dict, str]
    no_cache: bool = False
    GPU: bool = False

    def to_json(self):
        """Encode TrainRequestBody to a json object"""
        return json.dumps(self.__dict__, indent=4)

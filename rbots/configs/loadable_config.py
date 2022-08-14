from __future__ import annotations

import json
import logging
import os
from abc import ABC
from typing import Iterable, Optional

import yaml


class LoadableConfig(ABC):

    def __repr__(self) -> str:
        return str(self.__dict__)

    @classmethod
    def from_path(cls, path):
        split_path = path.split("::")
        filepath = split_path[0]
        data = dict()
        if filepath and os.path.exists(filepath):
            logging.debug(f"{str(cls).upper()} File found at path: {filepath}")
            if ".json" in filepath:
                with open(filepath, 'r') as fp:
                    data = json.load(fp)
            elif ".yaml" in filepath or ".yml" in filepath:
                with open(filepath, 'r') as fp:
                    data = yaml.safe_load(fp)
        if len(split_path)>1:
            for key in split_path[1].split(':'):
                data = data[key]
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def interpret(cls, val) -> Optional['LoadableConfig']:
        if isinstance(val, cls):
            return val
        elif not val:
            return None
        elif isinstance(val, str):
            return val
        elif isinstance(val, dict):
            return cls(**val)
        elif isinstance(val, Iterable):
            return [cls.interpret(v) for v in val]
        raise TypeError(
            f"Passed object of type {type(val)} is not interpretable")

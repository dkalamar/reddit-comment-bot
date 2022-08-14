

from ctypes import Union
from typing import SupportsFloat
from typing import Iterable
from rbots.configs.loadable_config import LoadableConfig


class QueryConfig(LoadableConfig):
    def __init__(self, keyphrase: Iterable[str], probability: SupportsFloat = 1, all: bool = False):
        self._keyphrase = keyphrase
        self._probability = probability
        self._all = all

    @property
    def keyphrase(self):
        return self._keyphrase

    @property
    def probability(self):
        return self._probability

    @property
    def all(self):
        return self._all

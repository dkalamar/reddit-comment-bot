from __future__ import annotations

from typing import Iterable, Union

from .loadable_config import LoadableConfig
from .query_config import QueryConfig


class ResponseConfig(LoadableConfig):
    """
    Response decision tree for Charbot
    """

    def __init__(self, response: Union[Iterable['ResponseConfig'], Iterable[str], str, None], query: QueryConfig) -> None:
        self._response = ResponseConfig.interpret(response)
        self._query = QueryConfig.interpret(query)

    @property
    def response(self) -> Union[Iterable['ResponseConfig'], Iterable[str], str, None]:
        return self._response

    @property
    def query(self) -> QueryConfig:
        return self._query

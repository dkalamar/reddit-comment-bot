from typing import Iterable, SupportsFloat

from rbots.configs import LoadableConfig, ResponseConfig


class CharBotConfig(LoadableConfig):
    def __init__(self, subreddits: Iterable[str], response: ResponseConfig, throttle: int = 0, rarity: SupportsFloat = 1):
        self._subreddits = subreddits
        self._throttle = throttle
        if rarity > 1:
            raise ValueError("Property 'rarity' must be between 0 and 1")
        self._rarity = rarity
        self._response = ResponseConfig.interpret(response)

    @property
    def response(self) -> ResponseConfig:
        return self._response

    @property
    def throttle(self) -> SupportsFloat:
        """
        Daily Limit for responses
        """
        return self._throttle

    @property
    def rarity(self) -> SupportsFloat:
        """
        Probablility to respond.
        """
        return self._rarity

    @property
    def subreddits(self) -> Iterable[str]:
        """
        Subreddits to scroll and contribute to
        """
        return self._subreddits

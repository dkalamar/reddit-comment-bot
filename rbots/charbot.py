import logging
from random import random
from typing import Optional, SupportsFloat, Tuple

import praw
from praw.models.reddit.comment import Comment

from rbots.commentbot import CommentBot
from rbots.configs import CharBotConfig
from rbots.configs.response_config import ResponseConfig


class CharBot(CommentBot):

    def __init__(self, reddit: praw.Reddit, config: CharBotConfig):
        self._config = config
        super().__init__(reddit)

    def evaluate_comment(self, comment: Comment) -> bool:
        return CharBot._evaluate_from_config(comment.body.lower(), self._config.response) and random() < self._config.rarity

    @staticmethod
    def _evaluate_from_config(message: str, config: ResponseConfig) -> bool:
        if not config:
            return False
        elif isinstance(config, str):
            return True
        elif config.query:
            passes = False
            if config.query.keyphrase:
                appears = [k in message
                           for k in config.query.keyphrase]
                passes = all(appears) if config.query.all else any(appears)
        if passes:
            for c in config.response:
                if CharBot._evaluate_from_config(message, c):
                    return True
        return False

    def generate_response(self, comment: Comment) -> str:
        _, response = CharBot._generate_from_config(
            comment.body.lower(), self._config.response)
        return response

    @staticmethod
    def _generate_from_config(message: str, config: ResponseConfig) -> Tuple[SupportsFloat, Optional[str]]:
        passes = False
        if not config:
            return 0, None
        elif isinstance(config, str):
            return 1, config
        elif config.query:
            if config.query.keyphrase:
                appears = [k in message
                           for k in config.query.keyphrase]
                passes = all(appears) if config.query.all else any(appears)
            else:
                passes = True
        if passes:
            responses = [CharBot._generate_from_config(
                message, c) for c in config.response]
            if responses:
                probability, texts = zip(*responses)
                rand = random()*sum(probability)
                total = 0
                for i, p in enumerate(probability):
                    total += p
                    if rand < total:
                        return config.query.probability, texts[i]
        return 0, None
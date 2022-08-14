from abc import ABC, abstractmethod
import logging
from typing import Optional
import praw
from praw.models.reddit.comment import Comment


class CommentBot(ABC):
    def __init__(self, reddit: praw.Reddit):
        self._reddit = reddit

    @property
    def reddit(self) -> praw.Reddit:
        return self._reddit

    def scroll(self, sub_name, dry_run=False, skip_existing=True):
        for comment in self.reddit.subreddit(sub_name).stream.comments(skip_existing=skip_existing):
            logging.info(f"Found comment {comment.id}")
            if self.evaluate_comment(comment) and comment.author != self._reddit.user.me() and self._reddit.user.me() not in [reply.author for reply in comment.replies]:
                response = self.generate_response(comment)
                _ = self._handle_response(comment, response, dry_run)

    def _handle_response(self, comment: Comment, response: str, dry_run=False) -> Optional[Comment]:
        logging.info(
            f"Responding to {comment.id}:'{comment.body}' with '{response}'")
        if response and not dry_run:
            return comment.reply(body=response)

    @abstractmethod
    def evaluate_comment(self, comment: Comment) -> bool:
        """
        Determine if bot should comment
        """
        pass

    @abstractmethod
    def generate_response(self, comment: Comment) -> str:
        """
        Create response to comment
        """
        pass

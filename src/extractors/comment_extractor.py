from time import timezone
from typing import List
from praw.models import Submission
from datetime import datetime, timezone

from src.models.comment_models import Comment


class CommentExtractor:
    """
    Responsible for extracting comments from a Reddit post.
    """

    @staticmethod
    def extract_comments(submission: Submission) -> List[Comment]:
        """
        Extracts all comments from a post.

        Args:
        submission: PRAW Submission object representing the post.

        Returns:
        A list of Comment objects.
        """
        submission.comment_sort = "top"
        submission.comments.replace_more(limit=None)

        comments = []

        for comment in submission.comments.list():
            comments.append(
                Comment(
                    author=str(comment.author),
                    text=comment.body,
                    created_utc=datetime.fromtimestamp(comment.created_utc, tz=timezone.utc),
                    ups=comment.ups
                )
            )

        return comments

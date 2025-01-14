from time import timezone
from typing import List
from praw.models import Submission
from datetime import datetime, timezone
from praw.exceptions import PRAWException

from old.models.comment_models import Comment
from old.utils.logger import logger


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
        try:
            submission.comment_sort = "top"
            submission.comments.replace_more(limit=None)

            comments = []

            for comment in submission.comments:
                comments.append(
                    Comment(
                        author=str(comment.author),
                        text=comment.body,
                        created_utc=datetime.fromtimestamp(comment.created_utc, tz=timezone.utc),
                        ups=comment.ups
                    )
                )

            return comments
        except PRAWException as e:
            logger.error(f"Erro ao extrair comentários do post {submission.id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao extrair comentários do post {submission.id}: {e}")
            return []

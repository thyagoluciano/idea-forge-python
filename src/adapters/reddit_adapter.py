# src/adapters/reddit_adapter.py
from typing import List, Optional, Any, Generator
from datetime import datetime
import praw
from src.config.config import Config
from src.core.ports.reddit_gateway import RedditGateway
from src.core.entities import Post, Comment
from src.core.utils.logger import setup_logger
from src.core.utils.reddit_helpers import RedditHelpers
from praw.exceptions import PRAWException

logger = setup_logger(__name__)


class RedditAdapter(RedditGateway):
    def __init__(self):
        self.config = Config()
        try:
            self.reddit = praw.Reddit(
                client_id=self.config.REDDIT_CLIENT_ID,
                client_secret=self.config.REDDIT_CLIENT_SECRET,
                user_agent=self.config.REDDIT_USER_AGENT
            )
            logger.info("Conexão com Reddit estabelecida com sucesso.")
        except praw.exceptions.PRAWException as e:
            logger.error(f"Erro ao conectar com o Reddit: {e}")
            self.reddit = None

    def _fetch_posts_from_listing(self, listing_generator: Any, batch_size: int, limit: Optional[int] = None) -> Generator[List[Post], None, None]:
        """
            Fetch posts from a listing generator and transforms them into Post objects.

            Args:
                listing_generator: A PRAW ListingGenerator.
                batch_size: Number of posts per batch.
                limit: Optional limit of posts to fetch.

            Yields:
                A list of Post objects.
            """
        posts = []
        posts_count = 0
        try:
            for submission in listing_generator:
                comments = self._extract_comments(submission)
                post = self._transform_submission_to_post(submission, comments)
                posts.append(post)
                posts_count += 1

                if len(posts) >= batch_size:
                    yield posts
                    posts = []
                if limit and posts_count >= limit:
                    yield posts
                    return
            if posts:
                yield posts
        except PRAWException as e:
            logger.error(f"Erro ao buscar posts: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar posts: {e}")

    @staticmethod
    def _transform_submission_to_post(submission, comments: List[Comment]) -> Post:
        """Transforms a PRAW submission object into a Post object."""
        return Post(
            title=submission.title,
            id=submission.id,
            url=submission.url,
            text=submission.selftext,
            num_comments=submission.num_comments,
            ups=submission.ups,
            comments=comments,
        )

    def _extract_comments(self, submission) -> List[Comment]:
        try:
            submission.comment_sort = "top"
            submission.comments.replace_more(limit=None)

            comments = []
            for comment in submission.comments:
                comments.append(
                    self._transform_comment_to_comment(comment)
                )
            return comments
        except PRAWException as e:
            logger.error(f"Erro ao extrair comentários do post {submission.id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao extrair comentários do post {submission.id}: {e}")
            return []

    @staticmethod
    def _transform_comment_to_comment(comment) -> Comment:
        """Transforms a PRAW comment object into a Comment object."""
        return Comment(
            author=str(comment.author),
            text=comment.body,
            created_utc=datetime.fromtimestamp(comment.created_utc),
            ups=comment.ups
        )

    def fetch_posts_from_subreddit(
            self,
            subreddit_name: str,
            sort_criteria: str,
            batch_size: int = 10,
            days_ago: int = 1,
            limit: Optional[int] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
    ) -> List[Post]:
        """
        Extracts posts from a specific subreddit.
        """
        if self.reddit is None:
            logger.error("Reddit não inicializado, impossível buscar posts.")
            return []
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            listing_generator = RedditHelpers.get_listing_generator_by_sort(
                self.reddit, subreddit, sort_criteria, start_date, end_date
            )
            posts = []
            for batch in self._fetch_posts_from_listing(listing_generator, batch_size, limit):
                posts.extend(batch)
            return posts
        except PRAWException as e:
            logger.error(f"Erro ao acessar o subreddit {subreddit_name}: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao extrair posts do subreddit {subreddit_name}: {e}")
            return []

    def fetch_posts_from_search(
            self,
            query: str,
            sort_criteria: str,
            batch_size: int = 10,
            days_ago: int = 1,
            limit: Optional[int] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
    ) -> List[Post]:
        """
        Extracts posts from Reddit using a search.
        """
        if self.reddit is None:
            logger.error("Reddit não inicializado, impossível buscar posts.")
            return []

        try:
            listing_generator = RedditHelpers.get_search_listing_generator_by_sort(
                self.reddit, query, sort_criteria, start_date, end_date
            )
            posts = []
            for batch in self._fetch_posts_from_listing(listing_generator, batch_size, limit):
                posts.extend(batch)
            return posts
        except PRAWException as e:
            logger.error(f"Erro ao executar a busca por {query}: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar posts: {e}")
            return []

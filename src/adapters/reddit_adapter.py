# src/adapters/reddit_adapter.py
from typing import List, Optional, Any
from datetime import datetime
import praw
from src.config.config import Config
from src.core.ports.reddit_gateway import RedditGateway
from src.core.entities import Post, Comment
from src.core.utils.logger import setup_logger
from src.core.utils.date_time import get_start_end_timestamps
from src.core.utils.reddit_helpers import RedditHelpers
from praw.exceptions import PRAWException
from time import timezone

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

    def _fetch_posts(self, listing_generator: Any, batch_size: int, start_timestamp: Optional[int] = None,
                     end_timestamp: Optional[int] = None, limit: Optional[int] = None) -> List[Post]:
        posts = []
        posts_count = 0

        try:
            for submission in listing_generator:
                comments = self._extract_comments(submission)
                post = Post(
                    title=submission.title,
                    id=submission.id,
                    url=submission.url,
                    text=submission.selftext,
                    num_comments=submission.num_comments,
                    ups=submission.ups,
                    comments=comments,
                )
                posts.append(post)
                posts_count += 1
                if len(posts) >= batch_size:
                    yield posts
                    posts = []

            if posts:
                yield posts
        except PRAWException as e:
            logger.error(f"Erro ao buscar posts: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar posts: {e}")
            return []

    def _extract_comments(self, submission) -> List[Comment]:
        try:
            submission.comment_sort = "top"
            submission.comments.replace_more(limit=None)

            comments = []

            for comment in submission.comments:
                comments.append(
                    Comment(
                        author=str(comment.author),
                        text=comment.body,
                        created_utc=datetime.fromtimestamp(comment.created_utc),
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

        Args:
        subreddit_name: Name of the subreddit.
        sort_criteria: Sort criteria ('hot', 'top', 'new', 'controversial').
        batch_size: Number of posts per page.
        days_ago: Number of days to go back.
        start_date: Start date for filtering posts (optional).
        end_date: End date for filtering posts (optional).

        Yields: Lists of Post objects.
        """
        if self.reddit is None:
            logger.error("Reddit não inicializado, impossível buscar posts.")
            return []

        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            start_timestamp, end_timestamp = get_start_end_timestamps(days_ago)
            listing_generator = RedditHelpers.get_listing_generator_by_sort(
                self.reddit, subreddit, sort_criteria, start_date, end_date
            )
            posts = []
            for batch in self._fetch_posts(listing_generator, batch_size, start_timestamp, end_timestamp, limit):
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

        Args:
        query: Search term.
        sort_criteria: Sorting criteria ('relevance', 'top', 'new', 'comments').
        batch_size: Number of posts per page.
        days_ago: Number of days to go back.
        start_date: Start date for filtering posts (optional).
        end_date: End date for filtering posts (optional).

        Yields:
        Lists of Post objects.
        """
        if self.reddit is None:
            logger.error("Reddit não inicializado, impossível buscar posts.")
            return []

        try:
            start_timestamp, end_timestamp = get_start_end_timestamps(days_ago)
            listing_generator = RedditHelpers.get_search_listing_generator_by_sort(
                self.reddit, query, sort_criteria, start_date, end_date
            )
            posts = []
            for batch in self._fetch_posts(listing_generator, batch_size, start_timestamp, end_timestamp, limit):
                posts.extend(batch)
            return posts
        except PRAWException as e:
            logger.error(f"Erro ao executar a busca por {query}: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar posts: {e}")
            return []

# extractors/post_extractor.py

from typing import List, Optional, Iterator, Any
from praw import Reddit
from praw.exceptions import PRAWException
from datetime import datetime, timedelta

from src.extractors.comment_extractor import CommentExtractor
from src.models.post_models import Post
from src.utils.date_time import get_utc_timestamp, get_start_end_timestamps
from src.utils.logger import logger
from src.utils.reddit_helpers import RedditHelpers


class PostExtractor:
    """
    Responsible for extracting posts from Reddit.
    """

    # Constantes para critérios de ordenação de posts
    SORT_CRITERIA_SUBREDDIT = ["hot", "top", "new", "controversial"]
    SORT_CRITERIA_SEARCH = ["relevance", "top", "new", "comments"]

    def __init__(self, reddit_client: Reddit):
        self.reddit = reddit_client
        self.comment_extractor = CommentExtractor()

    def _fetch_posts(self, listing_generator: Iterator[Any], batch_size: int, start_timestamp: Optional[int] = None,
                     end_timestamp: Optional[int] = None, limit: Optional[int] = None):
        """
        Helper function to search for posts using a ListingGenerator
        """

        posts = []
        posts_count = 0

        try:
            for submission in listing_generator:
                # Uncomment the following lines if you want to use timestamp filtering
                # if start_timestamp and end_timestamp:
                #     if get_utc_timestamp(submission.created_utc) < start_timestamp:
                #         break
                #     if get_utc_timestamp(submission.created_utc) > end_timestamp:
                #         continue
                comments = self.comment_extractor.extract_comments(submission)
                posts.append(
                    Post(
                        title=submission.title,
                        id=submission.id,
                        url=submission.url,
                        text=submission.selftext,
                        num_comments=submission.num_comments,
                        ups=submission.ups,
                        comments=comments,
                    )
                )
                posts_count += 1
                if len(posts) >= batch_size:
                    yield posts
                    posts = []

                if limit and posts_count >= limit:
                    break
            if posts:
                yield posts
        except PRAWException as e:
            logger.error(f"Erro ao buscar posts: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar posts: {e}")
            return []

    def extract_posts_from_subreddit(
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
        if sort_criteria not in self.SORT_CRITERIA_SUBREDDIT:
            raise ValueError(
                f"Invalid sort criteria: {sort_criteria}. Choose from {self.SORT_CRITERIA_SUBREDDIT}."
            )
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            start_timestamp, end_timestamp = get_start_end_timestamps(days_ago)
            listing_generator = RedditHelpers.get_listing_generator_by_sort(
                self.reddit, subreddit, sort_criteria, start_date, end_date
            )

            yield from self._fetch_posts(listing_generator, batch_size, start_timestamp, end_timestamp, limit)
        except PRAWException as e:
            logger.error(f"Erro ao acessar o subreddit {subreddit_name}: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao extrair posts do subreddit {subreddit_name}: {e}")
            return []

    def extract_posts_from_search(
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
        if sort_criteria not in self.SORT_CRITERIA_SEARCH:
            raise ValueError(
                f"Invalid search sort criteria: {sort_criteria}. Choose from {self.SORT_CRITERIA_SEARCH}."
            )
        try:
            start_timestamp, end_timestamp = get_start_end_timestamps(days_ago)
            listing_generator = RedditHelpers.get_search_listing_generator_by_sort(
                self.reddit, query, sort_criteria, start_date, end_date
            )
            yield from self._fetch_posts(listing_generator, batch_size, start_timestamp, end_timestamp, limit)
        except PRAWException as e:
            logger.error(f"Erro ao executar a busca por {query}: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar posts: {e}")
            return []

from typing import List, Optional, Iterator, Any
from praw import Reddit
from praw.models import Subreddit
from praw.exceptions import PRAWException

from src.extractors.comment_extractor import CommentExtractor
from src.models.post_models import Post
from src.utils.date_time import get_start_end_timestamps
from src.utils.logger import logger


class PostExtractor:
    """
    Responsible for extracting posts from Reddit.
    """

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
    ) -> List[Post]:
        """
        Extracts posts from a specific subreddit.

        Args:
        subreddit_name: Name of the subreddit.
        sort_criteria: Sort criteria ('hot', 'top', 'new', 'controversial').
        batch_size: Number of posts per page.
        days_ago: Number of days to go back.

        Yields: Lists of Post objects.
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            start_timestamp, end_timestamp = get_start_end_timestamps(days_ago)
            listing_generator = self._get_listing_generator_by_sort(subreddit, sort_criteria)

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
    ) -> List[Post]:
        """
        Extracts posts from Reddit using a search.

        Args:
        query: Search term.
        sort_criteria: Sorting criteria ('relevance', 'top', 'new', 'comments').
        batch_size: Number of posts per page.
        days_ago: Number of days to go back.

        Yields:
        Lists of Post objects.
        """
        try:
            start_timestamp, end_timestamp = get_start_end_timestamps(days_ago)
            listing_generator = self._get_search_listing_generator_by_sort(query, sort_criteria)
            yield from self._fetch_posts(listing_generator, batch_size, start_timestamp, end_timestamp, limit)
        except PRAWException as e:
             logger.error(f"Erro ao executar a busca por {query}: {e}")
             return []
        except Exception as e:
             logger.error(f"Erro inesperado ao buscar posts: {e}")
             return []
    @staticmethod
    def _get_listing_generator_by_sort(subreddit: Subreddit, sort_criteria: str):
        """
        Returns the Listing Generator based on the sort criteria
        """

        if sort_criteria == "hot":
            return subreddit.hot()
        elif sort_criteria == "top":
            return subreddit.top()
        elif sort_criteria == "new":
            return subreddit.new()
        elif sort_criteria == "controversial":
            return subreddit.controversial()
        else:
            raise ValueError(
                "Invalid sort criteria. Choose from 'hot', 'top', 'new', 'controversial'."
            )

    def _get_search_listing_generator_by_sort(self, query: str, sort_criteria: str):
        """
        Returns the Listing Generator based on the sort criteria for the search
        """
        if sort_criteria == "relevance":
            return self.reddit.subreddit("all").search(query, sort="relevance")
        elif sort_criteria == "top":
            return self.reddit.subreddit("all").search(query, sort="top")
        elif sort_criteria == "new":
            return self.reddit.subreddit("all").search(query, sort="new")
        elif sort_criteria == "comments":
            return self.reddit.subreddit("all").search(query, sort="comments")
        else:
            raise ValueError(
                "Invalid search sort criteria. Choose from 'relevance', 'top', 'new', 'comments'."
            )

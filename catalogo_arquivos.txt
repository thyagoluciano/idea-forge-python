## requirements.txt
```text
praw
python-dotenv
google-generativeai
psycopg2-binary
apscheduler
```

## docker-compose.yml
```yaml
services:
  postgres:
    image: postgres:17.2-alpine
    container_name: postgres
    restart: always
    environment:
      POSTGRES_DB: idea_forge
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## main.py
```python
from datetime import datetime, timedelta
import json

from src.core.reddit_client import RedditClient
from src.extractors.post_extractor import PostExtractor


def main():
    reddit_client = RedditClient()
    reddit_instance = reddit_client.get_reddit_instance()
    post_extractor = PostExtractor(reddit_instance)

    # Exemplo de uso para extrair posts de um subreddit
    subreddit_name = "SaaS"
    sort_criteria = "hot"
    batch_size = 5
    days_ago = 1
    limit = 1

    # Definir intervalo de datas
    start_date = datetime.now() - timedelta(days=2)  # Posts dos últimos 30 dias
    end_date = datetime.now()

    # Extrair posts de um subreddit com filtro de data
    for posts in post_extractor.extract_posts_from_subreddit(
        subreddit_name,
        sort_criteria,
        batch_size,
        start_date=start_date,
        end_date=end_date
    ):
        for post in posts:
            print(f"Post ID: {post.id}, \nTitle: {post.title}, \nDescription: {post.text}, \nURL: {post.url} \nUpvotes: {post.ups}, \nComments: {post.num_comments}")
            for comment in post.comments:
                print(f"   Comment Author: {comment.author}, Text: {comment.text}, Upvotes: {comment.ups}")
            print("--------------------------")


    # for posts in post_extractor.extract_posts_from_subreddit(subreddit_name, sort_criteria, batch_size, days_ago, limit):
    #     for post in posts:
    #         print(f"Post ID: {post.id}, \nTitle: {post.title}, \nDescription: {post.text}, \nURL: {post.url} \nUpvotes: {post.ups}, \nComments: {post.num_comments}")
    #         for comment in post.comments:
    #             print(f"   Comment Author: {comment.author}, Text: {comment.text}, Upvotes: {comment.ups}")
    #         print("--------------------------")

    # Exemplo de uso para extrair posts por pesquisa
    # query = "eleições 2022"
    # sort_criteria = "relevance"
    # batch_size = 5
    # days_ago = 1
    #
    # for posts in post_extractor.extract_posts_from_search(query, sort_criteria, batch_size, days_ago):
    #     for post in posts:
    #         print(f"Post ID: {post.id}, Title: {post.title}, Upvotes: {post.ups}, Comments: {post.num_comments}")
    #         for comment in post.comments:
    #             print(f"   Comment Author: {comment.author}, Text: {comment.text}, Upvotes: {comment.ups}")
    #         print("--------------------------")


if __name__ == "__main__":
    main()

```

## src/__init__.py
```python

```

## src/core/__init__.py
```python

```

## src/core/reddit_client.py
```python
import praw

from src.config.config import Config
from src.utils.logger import logger


class RedditClient:
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

    def get_reddit_instance(self):
        """Returns the PRAW Reddit instance."""
        return self.reddit
    
```

## src/config/config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Reddit API
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

    # Gemini API
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", 'gemini-pro')  # Default gemini-pro

    # Project Settings
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME", "Entrepreneur")
    LIMIT_POSTS = os.getenv("LIMIT_POSTS", 10)
    SORT_TYPE = os.getenv("SORT_TYPE", 'hot')

    # PostgreSQL Database
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "idea_forge")

    def __post_init__(self):
        self._validate_required_vars()

    def _validate_required_vars(self):
        """Validate required environment variables."""
        required_vars = {
            "REDDIT_CLIENT_ID": self.REDDIT_CLIENT_ID,
            "REDDIT_CLIENT_SECRET": self.REDDIT_CLIENT_SECRET,
            "REDDIT_USER_AGENT": self.REDDIT_USER_AGENT,
            "POSTGRES_USER": self.POSTGRES_USER,
            "POSTGRES_PASSWORD": self.POSTGRES_PASSWORD
        }

        for var, value in required_vars.items():
            if not value:
                raise ValueError(f"Missing required environment variable: {var}")

```

## src/config/__init__.py
```python

```

## src/utils/reddit_helpers.py
```python
# utils/reddit_helpers.py

from praw import Reddit
from praw.models import Subreddit
from datetime import datetime, timedelta


class RedditHelpers:

    @staticmethod
    def get_listing_generator_by_sort(reddit_instance: Reddit, subreddit: Subreddit, sort_criteria: str,
                                      start_date: datetime = None, end_date: datetime = None):
        """
        Returns the Listing Generator based on the sort criteria for subreddits.
        """
        listing = None
        if sort_criteria == "hot":
            listing = subreddit.hot()
        elif sort_criteria == "top":
            listing = subreddit.top()
        elif sort_criteria == "new":
            listing = subreddit.new()
        elif sort_criteria == "controversial":
            listing = subreddit.controversial()
        else:
            raise ValueError(
                "Invalid sort criteria. Choose from 'hot', 'top', 'new', 'controversial'."
            )

        return RedditHelpers.filter_by_date(listing, start_date, end_date)

    @staticmethod
    def get_search_listing_generator_by_sort(reddit_instance: Reddit, query: str, sort_criteria: str,
                                             start_date: datetime = None, end_date: datetime = None):
        """
        Returns the Listing Generator based on the sort criteria for search.
        """
        listing = None
        if sort_criteria == "relevance":
            listing = reddit_instance.subreddit("all").search(query, sort="relevance")
        elif sort_criteria == "top":
            listing = reddit_instance.subreddit("all").search(query, sort="top")
        elif sort_criteria == "new":
            listing = reddit_instance.subreddit("all").search(query, sort="new")
        elif sort_criteria == "comments":
            listing = reddit_instance.subreddit("all").search(query, sort="comments")
        else:
            raise ValueError(
                "Invalid search sort criteria. Choose from 'relevance', 'top', 'new', 'comments'."
            )

        return RedditHelpers.filter_by_date(listing, start_date, end_date)

    @staticmethod
    def filter_by_date(listing, start_date: datetime = None, end_date: datetime = None):
        """
        Filters the listing by date range.
        """
        if start_date or end_date:
            return (
                post for post in listing
                if (not start_date or datetime.fromtimestamp(post.created_utc) >= start_date) and
                   (not end_date or datetime.fromtimestamp(post.created_utc) <= end_date)
            )

        return listing

```

## src/utils/__init__.py
```python

```

## src/utils/logger.py
```python
import logging


def setup_logger(name, log_file='app.log', level=logging.INFO):
    """Sets and returns a logger."""
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


logger = setup_logger('ideaForge')

```

## src/utils/date_time.py
```python
import datetime
from datetime import datetime, timedelta, timezone


def get_utc_timestamp(date):
    if isinstance(date, float):
        date = datetime.fromtimestamp(date, tz=timezone.utc)
    return int(date.timestamp())


def get_start_end_timestamps(days_ago):
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days_ago)

    return get_utc_timestamp(start_date), get_utc_timestamp(end_date)

```

## src/utils/helpers.py
```python
import re


def clean_text(text):
    """Remove line breaks, extra spaces, and special characters from text."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

```

## src/models/post_models.py
```python
from dataclasses import dataclass
from typing import List

from src.models.comment_models import Comment


@dataclass
class Post:
    """Represents a Reddit post."""
    title: str
    id: str
    url: str
    text: str
    num_comments: int
    ups: int
    comments: List[Comment]
```

## src/models/comment_models.py
```python
import datetime
from dataclasses import dataclass


@dataclass
class Comment:
    """Represents a Reddit comment."""
    author: str
    text: str
    created_utc: datetime
    ups: int

```

## src/models/__init__.py
```python

```

## src/extractors/post_extractor.py
```python
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

```

## src/extractors/comment_extractor.py
```python
from time import timezone
from typing import List
from praw.models import Submission
from datetime import datetime, timezone
from praw.exceptions import PRAWException

from src.models.comment_models import Comment
from src.utils.logger import logger


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
        except PRAWException as e:
            logger.error(f"Erro ao extrair comentários do post {submission.id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao extrair comentários do post {submission.id}: {e}")
            return []

```

## src/extractors/__init__.py
```python

```


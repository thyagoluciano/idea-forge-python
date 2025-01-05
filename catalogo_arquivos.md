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

import json

from src.core.reddit_client import RedditClient
from src.extractors.post_extractor import PostExtractor


def main():
    reddit_client = RedditClient()
    reddit_instance = reddit_client.get_reddit_instance()
    post_extractor = PostExtractor(reddit_instance)

    # Exemplo de uso para extrair posts de um subreddit
    subreddit_name = "brasil"
    sort_criteria = "top"
    batch_size = 5
    days_ago = 1

    for posts in post_extractor.extract_posts_from_subreddit(subreddit_name, sort_criteria, batch_size, days_ago):
        for post in posts:
            print(f"Post ID: {post.id}, Title: {post.title}, Upvotes: {post.ups}, Comments: {post.num_comments}")
            for comment in post.comments:
               print(f"   Comment Author: {comment.author}, Text: {comment.text}, Upvotes: {comment.ups}")
            print("--------------------------")

    # Exemplo de uso para extrair posts por pesquisa
    query = "eleições 2022"
    sort_criteria = "relevance"
    batch_size = 5
    days_ago = 1

    for posts in post_extractor.extract_posts_from_search(query, sort_criteria, batch_size, days_ago):
         for post in posts:
            print(f"Post ID: {post.id}, Title: {post.title}, Upvotes: {post.ups}, Comments: {post.num_comments}")
            for comment in post.comments:
               print(f"   Comment Author: {comment.author}, Text: {comment.text}, Upvotes: {comment.ups}")
            print("--------------------------")


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

```

## src/config/__init__.py
```python

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
from typing import List, Optional, Iterator, Any
from praw import Reddit
from praw.models import Subreddit

from src.extractors.comment_extractor import CommentExtractor
from src.models.post_models import Post
from src.utils.date_time import get_utc_timestamp, get_start_end_timestamps


class PostExtractor:
    """
    Responsible for extracting posts from Reddit.
    """

    def __init__(self, reddit_client: Reddit):
        self.reddit = reddit_client
        self.comment_extractor = CommentExtractor()

    def _fetch_posts(self, listing_generator: Iterator[Any], batch_size: int, start_timestamp: Optional[int] = None,
                     end_timestamp: Optional[int] = None):
        """
        Helper function to search for posts using a ListingGenerator
        """

        posts = []

        for submission in listing_generator:
            if start_timestamp and end_timestamp:
                if get_utc_timestamp(submission.created_utc) < start_timestamp:
                    break
                if get_utc_timestamp(submission.created_utc) > end_timestamp:
                    continue

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
            if len(posts) >= batch_size:
                yield posts
                posts = []
        if posts:
            yield posts

    def extract_posts_from_subreddit(
            self,
            subreddit_name: str,
            sort_criteria: str,
            batch_size: int = 10,
            days_ago: int = 7,
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
        subreddit = self.reddit.subreddit(subreddit_name)
        start_timestamp, end_timestamp = get_start_end_timestamps(days_ago)
        listing_generator = self._get_listing_generator_by_sort(subreddit, sort_criteria)

        yield from self._fetch_posts(listing_generator, batch_size, start_timestamp, end_timestamp)

    def extract_posts_from_search(
            self,
            query: str,
            sort_criteria: str,
            batch_size: int = 10,
            days_ago: int = 7,
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
        start_timestamp, end_timestamp = get_start_end_timestamps(days_ago)
        listing_generator = self._get_search_listing_generator_by_sort(query, sort_criteria)
        yield from self._fetch_posts(listing_generator, batch_size, start_timestamp, end_timestamp)


    def _get_listing_generator_by_sort(self, subreddit: Subreddit, sort_criteria: str):
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

```

## src/extractors/comment_extractor.py
```python
from typing import List
from praw.models import Submission
from datetime import datetime

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
        comments = []
        submission.comment_sort = "top"
        submission.comments.replace_more(limit=None)

        for comment in submission.comments.list():
            comments.append(
                Comment(
                    author=str(comment.author),
                    text=comment.body,
                    created_utc=datetime.fromtimestamp(comment.created_utc),
                    ups=comment.ups
                )
            )

        return comments

```

## src/extractors/__init__.py
```python

```


## conftest.py
```python
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
```

## requirements.txt
```text
praw~=7.8.1
python-dotenv~=1.0.1
google-generativeai
psycopg2-binary
sqlalchemy~=2.0.36
apscheduler~=3.11.0
protobuf~=5.29.1
requests~=2.32.3
pytest~=8.3.4
fastapi~=0.115.6
pydantic~=2.10.4
uvicorn~=0.34.0
```

## Dockerfile
```
# --- Stage 1: Builder Stage ---
FROM python:3.11-alpine3.19 AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev build-base

# Copy only requirements file
COPY requirements.txt .

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final Stage ---
FROM python:3.11-alpine3.19

WORKDIR /app

# Copy application from builder stage
COPY --from=builder /app /app

# Copy source code
COPY . .

# Remove unnecessary files
RUN rm -rf __pycache__ && \
    find . -name "*.pyc" -delete && \
    find . -name "*.pyo" -delete

# Run application
CMD ["python", "src/main.py"]
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

## .pytest_cache/CACHEDIR.TAG
```
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag created by pytest.
# For information about cache directory tags, see:
#	https://bford.info/cachedir/spec.html

```

## .pytest_cache/v/cache/nodeids
```
[
  "tests/adapters/test_extraction_scheduler.py::test_extraction_scheduler_run_now",
  "tests/adapters/test_extraction_scheduler.py::test_extraction_scheduler_start_and_run",
  "tests/adapters/test_reddit_adapter.py::test_fetch_posts_from_search",
  "tests/adapters/test_reddit_adapter.py::test_fetch_posts_from_search_with_error",
  "tests/adapters/test_reddit_adapter.py::test_fetch_posts_from_subreddit",
  "tests/adapters/test_reddit_adapter.py::test_fetch_posts_from_subreddit_with_error",
  "tests/core/use_cases/test_extraction_use_case.py::test_extract_posts_from_search",
  "tests/core/use_cases/test_extraction_use_case.py::test_extract_posts_from_subreddit"
]
```

## .pytest_cache/v/cache/lastfailed
```
{
  "tests/adapters/test_extraction_scheduler.py::test_extraction_scheduler_start_and_run": true,
  "tests/adapters/test_extraction_scheduler.py::test_extraction_scheduler_run_now": true,
  "tests/adapters/test_reddit_adapter.py::test_fetch_posts_from_subreddit": true
}
```

## .pytest_cache/v/cache/stepwise
```
[]
```

## tests/core/use_cases/test_extraction_use_case.py
```python
import pytest
from unittest.mock import Mock
from datetime import datetime
from src.core.use_cases.extraction_use_case import ExtractionUseCase
from src.core.entities import Post, Comment


@pytest.fixture
def mock_reddit_gateway():
    """Fixture para criar um mock do RedditGateway."""
    mock = Mock()
    mock.fetch_posts_from_subreddit.return_value = [
        Post(title="Test Post 1", id="1", url="http://test1", text="test", num_comments=0, ups=0, comments=[]),
        Post(title="Test Post 2", id="2", url="http://test2", text="test", num_comments=0, ups=0, comments=[])
    ]
    mock.fetch_posts_from_search.return_value = [
        Post(title="Test Search Post 1", id="1", url="http://test1", text="test", num_comments=0, ups=0, comments=[]),
        Post(title="Test Search Post 2", id="2", url="http://test2", text="test", num_comments=0, ups=0, comments=[])
    ]
    return mock
@pytest.fixture
def mock_database_gateway():
    """Fixture para criar um mock do DatabaseGateway."""
    mock = Mock()
    return mock


def test_extract_posts_from_subreddit(mock_reddit_gateway, mock_database_gateway):
    """Testa a extração de posts de um subreddit."""
    extraction_use_case = ExtractionUseCase(mock_reddit_gateway, mock_database_gateway)
    posts = extraction_use_case.extract_posts_from_subreddit(
        subreddit_name="test_subreddit",
        sort_criteria="hot",
        batch_size=10,
        days_ago=1,
        limit=None
    )
    assert len(posts) == 2
    mock_reddit_gateway.fetch_posts_from_subreddit.assert_called_once()
    mock_database_gateway.add_post.assert_called()

def test_extract_posts_from_search(mock_reddit_gateway, mock_database_gateway):
    """Testa a extração de posts de um subreddit."""
    extraction_use_case = ExtractionUseCase(mock_reddit_gateway, mock_database_gateway)
    posts = extraction_use_case.extract_posts_from_search(
        query="test_query",
        sort_criteria="relevance",
        batch_size=10,
        days_ago=1,
        limit=None
    )
    assert len(posts) == 2
    mock_reddit_gateway.fetch_posts_from_search.assert_called_once()
    mock_database_gateway.add_post.assert_called()
```

## tests/core/use_cases/__pycache__/test_extraction_use_case.cpython-311-pytest-7.4.3.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## tests/adapters/test_reddit_adapter.py
```python
from unittest.mock import Mock, patch
import pytest
from src.adapters.reddit_adapter import RedditAdapter
from src.core.entities import Post, Comment
import praw


@pytest.fixture
def mock_praw_reddit():
    """Fixture para criar um mock do praw.Reddit."""
    mock_reddit = Mock()
    mock_subreddit = Mock()
    mock_submission = Mock()
    mock_submission.title = "Test Post"
    mock_submission.id = "test_id"
    mock_submission.url = "http://test.com"
    mock_submission.selftext = "Test text"
    mock_submission.num_comments = 0
    mock_submission.ups = 0
    mock_submission.comments = []

    mock_subreddit.hot.return_value = [mock_submission]
    mock_subreddit.top.return_value = [mock_submission]
    mock_subreddit.new.return_value = [mock_submission]
    mock_subreddit.controversial.return_value = [mock_submission]
    mock_reddit.subreddit.return_value = mock_subreddit

    mock_search = Mock()
    mock_search.search.return_value = [mock_submission]
    mock_reddit.subreddit.return_value = mock_search

    return mock_reddit


def test_fetch_posts_from_subreddit(mock_praw_reddit):
    """Testa a extração de posts de um subreddit."""
    with patch("src.adapters.reddit_adapter.praw.Reddit", return_value=mock_praw_reddit):
        reddit_adapter = RedditAdapter()
        posts = reddit_adapter.fetch_posts_from_subreddit(
            subreddit_name="test_subreddit",
            sort_criteria="hot",
            batch_size=10,
            days_ago=1,
            limit=10
        )
        assert len(posts) == 1
        assert isinstance(posts[0], Post)
        mock_praw_reddit.subreddit.assert_called_with("test_subreddit")
        mock_praw_reddit.subreddit().hot.assert_called_once()


def test_fetch_posts_from_search(mock_praw_reddit):
    """Testa a extração de posts de uma busca."""
    with patch("src.adapters.reddit_adapter.praw.Reddit", return_value=mock_praw_reddit):
        reddit_adapter = RedditAdapter()
        posts = reddit_adapter.fetch_posts_from_search(
             query="test_query",
            sort_criteria="relevance",
            batch_size=10,
            days_ago=1,
            limit=10
        )
        assert len(posts) == 1
        assert isinstance(posts[0], Post)
        mock_praw_reddit.subreddit.assert_called_with("all")
        mock_praw_reddit.subreddit().search.assert_called_once()

def test_fetch_posts_from_subreddit_with_error(mock_praw_reddit):
    """Testa a extração de posts de um subreddit."""
    mock_praw_reddit.subreddit.side_effect = praw.exceptions.PRAWException("Simulated PRAW Error")
    with patch("src.adapters.reddit_adapter.praw.Reddit", return_value=mock_praw_reddit):
        reddit_adapter = RedditAdapter()
        posts = reddit_adapter.fetch_posts_from_subreddit(
            subreddit_name="test_subreddit",
            sort_criteria="hot",
            batch_size=10,
            days_ago=1,
            limit=10
        )
        assert len(posts) == 0

def test_fetch_posts_from_search_with_error(mock_praw_reddit):
    """Testa a extração de posts de um subreddit."""
    mock_praw_reddit.subreddit.side_effect = praw.exceptions.PRAWException("Simulated PRAW Error")
    with patch("src.adapters.reddit_adapter.praw.Reddit", return_value=mock_praw_reddit):
        reddit_adapter = RedditAdapter()
        posts = reddit_adapter.fetch_posts_from_search(
             query="test_query",
            sort_criteria="relevance",
            batch_size=10,
            days_ago=1,
            limit=10
        )
        assert len(posts) == 0
```

## tests/adapters/test_extraction_scheduler.py
```python
from unittest.mock import patch
import pytest
from src.adapters.extraction_scheduler import ExtractionScheduler
from src.adapters.database_adapter import DatabaseAdapter
import time


@pytest.fixture
def mock_database_adapter():
    """Fixture para criar um mock do DatabaseGateway."""
    mock_adapter = DatabaseAdapter()
    return mock_adapter


def test_extraction_scheduler_start_and_run(mock_database_adapter):
    """Testa se o scheduler inicia e executa corretamente a extração."""
    config = {
        "type": "subreddit",
        "subreddit_name": "SaaS",
        "sort_criteria": "hot",
        "batch_size": 10,
        "days_ago": 1,
        "limit": 10,
        "schedule_time": "00:10",  # Horario da extração
        "daily": True,
        "enabled": True
    }
    mock_database_adapter.add_extraction_config(config)
    extraction_scheduler = ExtractionScheduler()

    with patch.object(extraction_scheduler, '_execute_extraction') as mock_execute_extraction:
        extraction_scheduler.start()
        time.sleep(2)
        extraction_scheduler.shutdown()
        assert mock_execute_extraction.call_count >= 1


def test_extraction_scheduler_run_now(mock_database_adapter):
    """Testa a execução imediata da extração."""
    config = {
        "type": "subreddit",
        "subreddit_name": "SaaS",
        "sort_criteria": "hot",
        "batch_size": 10,
        "days_ago": 1,
        "limit": 10,
        "schedule_time": "00:10",  # Horario da extração
        "daily": True,
        "enabled": True
    }
    mock_database_adapter.add_extraction_config(config)
    extraction_scheduler = ExtractionScheduler()

    with patch.object(extraction_scheduler, '_execute_extraction') as mock_execute_extraction:

        configs = mock_database_adapter.get_all_extraction_configs()
        for config in configs:
            if config.get("subreddit_name") == "SaaS":
                extraction_scheduler.run_extraction_now(config)
        time.sleep(2)
        assert mock_execute_extraction.call_count >= 1
        extraction_scheduler.shutdown()
```

## tests/adapters/__pycache__/test_reddit_adapter.cpython-311-pytest-7.4.3.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## tests/adapters/__pycache__/test_extraction_scheduler.cpython-311-pytest-7.4.3.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## __pycache__/conftest.cpython-311-pytest-7.4.3.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/__init__.py
```python

```

## src/main.py
```python
# src/main.py
import time
import threading
import uvicorn

from src.adapters.extraction_scheduler import ExtractionScheduler
from src.adapters.analysis_scheduler import AnalysisScheduler
from src.adapters.database_adapter import DatabaseAdapter
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    extraction_scheduler = ExtractionScheduler()
    extraction_thread = threading.Thread(target=extraction_scheduler.start)
    extraction_thread.start()

    # Inicia o scheduler de analise
    analysis_scheduler = AnalysisScheduler()
    analysis_thread = threading.Thread(target=analysis_scheduler.start)
    analysis_thread.start()

    # Força a execução imediata de uma extração

    # database_adapter = DatabaseAdapter()
    # configs = database_adapter.get_all_extraction_configs()
    # for config in configs:
    #     if config.subreddit_name == "SaaS":
    #         extraction_scheduler.run_extraction_now(config)
    #
    # analysis_scheduler.run_analysis_now()

    api_thread = threading.Thread(target=run_api)
    api_thread.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        extraction_scheduler.shutdown()
        analysis_scheduler.shutdown()
        extraction_thread.join()
        analysis_thread.join()


def run_api():
    """Runs the FastAPI application."""
    import src.adapters.api.main as api
    uvicorn.run(api.app, host="0.0.0.0", port=8081)


if __name__ == "__main__":
    main()

```

## src/database/__init__.py
```python

```

## src/database/models/post_models.py
```python
from dataclasses import dataclass
from typing import List

from old.models.comment_models import Comment


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

## src/database/models/database_models.py
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PostDB(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    text = Column(String)
    num_comments = Column(Integer)
    ups = Column(Integer)
    created_at = Column(DateTime)
    gemini_analysis = Column(Boolean, default=False)
    comments = relationship("CommentDB", back_populates="post", cascade="all, delete-orphan")


class CommentDB(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String)
    text = Column(String)
    created_utc = Column(DateTime)
    ups = Column(Integer)
    post_id = Column(String, ForeignKey("posts.id"))
    post = relationship("PostDB", back_populates="comments")


class SaasIdeaDB(Base):
    __tablename__ = "saas_ideas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    differentiators = Column(JSON)
    features = Column(JSON)
    implementation_score = Column(Integer)
    market_viability_score = Column(Integer)
    category = Column(String)
    post_id = Column(String, ForeignKey("posts.id"))
    post = relationship("PostDB")


class ExtractionConfigDB(Base):
    __tablename__ = "extraction_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False) # subreddit or search
    subreddit_name = Column(String)
    query = Column(String)
    sort_criteria = Column(String, nullable=False)
    batch_size = Column(Integer, default=10)
    days_ago = Column(Integer, default=1)
    limit = Column(Integer)
    schedule_time = Column(String) # Store time as HH:MM
    daily = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)
    last_run = Column(DateTime)

```

## src/database/models/comment_models.py
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

## src/database/models/__init__.py
```python

```

## src/database/models/__pycache__/database_models.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/database/models/__pycache__/__init__.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/database/__pycache__/__init__.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/__init__.py
```python

```

## src/core/entities.py
```python
# src/core/entities.py
from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Comment:
    """Represents a Reddit comment."""
    author: str
    text: str
    created_utc: datetime
    ups: int


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

## src/core/utils/reddit_helpers.py
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

## src/core/utils/__init__.py
```python

```

## src/core/utils/logger.py
```python
# src/core/utils/logger.py
import logging


def setup_logger(name, level=logging.INFO):
    """Sets and returns a logger."""
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
```

## src/core/utils/date_time.py
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

## src/core/utils/helpers.py
```python
import re


def clean_text(text):
    """Remove line breaks, extra spaces, and special characters from text."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

```

## src/core/utils/__pycache__/logger.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/utils/__pycache__/date_time.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/utils/__pycache__/__init__.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/utils/__pycache__/reddit_helpers.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/__pycache__/entities.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/__pycache__/__init__.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/use_cases/extraction_use_case.py
```python
# src/core/use_cases/extraction_use_case.py
from typing import List, Optional
from datetime import datetime
from src.core.ports.reddit_gateway import RedditGateway
from src.core.ports.database_gateway import DatabaseGateway
from src.core.entities import Post
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


class ExtractionUseCase:
    def __init__(self, reddit_gateway: RedditGateway, database_gateway: DatabaseGateway):
        self.reddit_gateway = reddit_gateway
        self.database_gateway = database_gateway

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
        logger.info(f"Iniciando extração de posts do subreddit {subreddit_name}")
        posts = self.reddit_gateway.fetch_posts_from_subreddit(
            subreddit_name, sort_criteria, batch_size, days_ago, limit, start_date, end_date
        )
        saved_posts = 0
        for post in posts:
            if limit and saved_posts >= limit:
                break
            self.database_gateway.add_post(post)
            saved_posts += 1
        logger.info(f"Extração de posts do subreddit {subreddit_name} finalizada. Total de posts: {saved_posts}")
        return posts

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
        logger.info(f"Iniciando extração de posts da busca {query}")
        posts = self.reddit_gateway.fetch_posts_from_search(
            query, sort_criteria, batch_size, days_ago, limit, start_date, end_date
        )
        saved_posts = 0
        for post in posts:
            if limit and saved_posts >= limit:
                break
            self.database_gateway.add_post(post)
            saved_posts += 1
        logger.info(f"Extração de posts da busca {query} finalizada. Total de posts: {saved_posts}")
        return posts

```

## src/core/use_cases/__init__.py
```python

```

## src/core/use_cases/analysis_use_case.py
```python
# src/core/use_cases/analysis_use_case.py
from typing import List, Optional
from src.core.ports.gemini_gateway import GeminiGateway
from src.core.ports.database_gateway import DatabaseGateway
from src.core.entities import Post
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


class AnalysisUseCase:
    def __init__(self, gemini_gateway: GeminiGateway, database_gateway: DatabaseGateway):
        self.gemini_gateway = gemini_gateway
        self.database_gateway = database_gateway

    def analyze_posts(self, batch_size: int = 10):
        offset = 0
        while True:
            posts = self.database_gateway.get_posts_to_analyze(batch_size)
            if not posts:
                logger.info("Não há mais posts para analisar.")
                break

            logger.info(f"Analisando lote de {len(posts)} posts. Offset: {offset}")
            for post in posts:
                try:
                    self._analyze_post(post)
                except Exception as e:
                    logger.error(f"Erro ao analisar post {post.id}: {e}")
            offset += batch_size

    def _analyze_post(self, post: Post):
        text_to_analyze = f"{post.title} \n {post.text} \n {' '.join([comment.text for comment in post.comments])}"
        gemini_analysis = self.gemini_gateway.analyze_text(text_to_analyze, post.title)
        self.database_gateway.add_saas_ideas(post.id, gemini_analysis)
        self.database_gateway.update_post_analysis(post.id)
        logger.info(f"Post {post.id} analyzed")
```

## src/core/use_cases/__pycache__/extraction_use_case.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/use_cases/__pycache__/__init__.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/ports/__init__.py
```python

```

## src/core/ports/gemini_gateway.py
```python
# src/core/ports/gemini_gateway.py
from abc import ABC, abstractmethod
from typing import Dict, Optional


class GeminiGateway(ABC):
    @abstractmethod
    def analyze_text(self, text: str, post_title: str) -> Optional[Dict]:
        pass
```

## src/core/ports/database_gateway.py
```python
# src/core/ports/database_gateway.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.entities import Post


class DatabaseGateway(ABC):
    @abstractmethod
    def add_post(self, post: Post) -> Optional[str]:
        pass

    @abstractmethod
    def add_saas_ideas(self, post_id: str, gemini_analysis: dict) -> None:
        pass

    @abstractmethod
    def post_exists(self, post_id: str) -> bool:
        pass

    @abstractmethod
    def post_already_analyzed(self, post_id: str) -> bool:
        pass

    @abstractmethod
    def add_extraction_config(self, config_data: dict) -> None:
        pass

    @abstractmethod
    def get_all_extraction_configs(self) -> List[dict]:
        pass

    @abstractmethod
    def update_extraction_config(self, config_id: int) -> None:
        pass

    @abstractmethod
    def update_post_analysis(self, post_id: str) -> None:
        pass
```

## src/core/ports/reddit_gateway.py
```python
# src/core/ports/reddit_gateway.py
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from src.core.entities import Post


class RedditGateway(ABC):
    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
    
```

## src/core/ports/saas_ideas_gateway.py
```python
# src/core/ports/saas_ideas_gateway.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict


class SaasIdeasGateway(ABC):
    @abstractmethod
    def list_saas_ideas(
            self,
            implementation_score: Optional[int] = None,
            market_viability_score: Optional[int] = None,
            category: Optional[str] = None,
            features: Optional[str] = None,
            differentiators: Optional[str] = None,
            description: Optional[str] = None,
            page: int = 1,
            page_size: int = 10,
            order_by: Optional[str] = None,
            order_direction: Optional[str] = "asc"
    ) -> Dict:
        pass

    @abstractmethod
    def list_all_categories(self) -> List[str]:
        pass
```

## src/core/ports/__pycache__/database_gateway.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/ports/__pycache__/reddit_gateway.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/core/ports/__pycache__/__init__.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
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

## src/config/__pycache__/config.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/config/__pycache__/__init__.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/__pycache__/__init__.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/adapters/analysis_scheduler.py
```python
# src/adapters/analysis_scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import threading

from src.adapters.database_adapter import DatabaseAdapter
from src.adapters.gemini_adapter import GeminiAdapter
from src.core.use_cases.analysis_use_case import AnalysisUseCase
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


def run_in_thread(func, *args, **kwargs):
    """Executes a function in a separate thread."""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread


class AnalysisScheduler:
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.database_adapter = DatabaseAdapter()
        self.gemini_adapter = GeminiAdapter()
        self.analysis_use_case = AnalysisUseCase(self.gemini_adapter, self.database_adapter)
        self.job_interval = 10  # intervalo entre os jobs em segundos
        self.batch_size = 10

    def start(self):
        """Starts the scheduler and adds existing jobs."""
        self._add_existing_jobs()
        self.scheduler.start()
        logger.info("Agendador de análise iniciado.")

    def _add_existing_jobs(self):
        """Adds all enabled analysis configurations as jobs."""
        # Por enquanto vamos adicionar apenas um job fixo
        self._add_job()

    def _add_job(self):
        """Adds a single job to the scheduler."""
        trigger = CronTrigger(minute="0")  # execute a cada hora
        self.scheduler.add_job(
            self._run_analysis,
            trigger=trigger,
            id="analysis_job",
            name=f"Analysis Job"
        )
        logger.info(f"Agendamento para análise adicionado")

    def _run_analysis(self):
        """Runs the analysis."""
        run_in_thread(self._execute_analysis)

    def _execute_analysis(self):
        """Executes the analysis and handle the interval."""
        logger.info("Iniciando análise dos posts.")
        try:
            self.analysis_use_case.analyze_posts(self.batch_size)
            logger.info("Análise dos posts finalizada com sucesso.")
        except Exception as e:
            logger.error(f"Erro durante a execução da análise dos posts: {e}")
        finally:
            time.sleep(self.job_interval)

    def run_analysis_now(self):
        """Runs the analysis immediately."""
        logger.info("Executando análise manualmente.")
        run_in_thread(self._execute_analysis)

    def shutdown(self):
        """Shuts down the scheduler."""
        self.scheduler.shutdown()
        logger.info("Agendador de análise finalizado.")
```

## src/adapters/__init__.py
```python

```

## src/adapters/extraction_scheduler.py
```python
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import threading

from src.adapters.database_adapter import DatabaseAdapter
from src.core.use_cases.extraction_use_case import ExtractionUseCase
from src.adapters.reddit_adapter import RedditAdapter
from src.database.models.database_models import ExtractionConfigDB
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


def run_in_thread(func, *args, **kwargs):
    """Executes a function in a separate thread."""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread


class ExtractionScheduler:
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.database_adapter = DatabaseAdapter()
        self.reddit_adapter = RedditAdapter()
        self.extraction_use_case = ExtractionUseCase(self.reddit_adapter, self.database_adapter)
        self.job_interval = 5  # intervalo entre os jobs em segundos

    def start(self):
        """Starts the scheduler and adds existing jobs."""
        self._add_existing_jobs()
        self.scheduler.start()
        logger.info("Agendador de extração iniciado.")

    def _add_existing_jobs(self):
        """Adds all enabled extraction configurations as jobs."""
        session = self.database_adapter.Session()
        try:
            configs = session.query(ExtractionConfigDB).filter(ExtractionConfigDB.enabled == True).all()
            for config in configs:
                self._add_job(config)
        except Exception as e:
            logger.error(f"Erro ao buscar subreddits no banco de dados: {e}")
        finally:
            session.close()

    def _add_job(self, config):
        """Adds a single job to the scheduler."""
        if config.daily and config.schedule_time:
            trigger = CronTrigger(hour=config.schedule_time.split(":")[0], minute=config.schedule_time.split(":")[1])
        else:
            # TODO: implementar agendamento por intervalo
            raise ValueError("Agendamento por intervalo não implementado")
        self.scheduler.add_job(
            self._run_extraction,
            trigger=trigger,
            args=[config],
            id=str(config.id),
            name=f"Extraction Job {config.id}"
        )
        logger.info(f"Agendamento para extração com ID {config.id} adicionado")

    def _run_extraction(self, config):
        """Runs the extraction based on the config."""
        run_in_thread(self._execute_extraction, config)

    def _execute_extraction(self, config):
        """Executes the extraction and handle the interval."""
        logger.info(f"Iniciando extração com ID {config.id}")
        try:
            if config.type == "subreddit":
                 self.extraction_use_case.extract_posts_from_subreddit(
                     config.subreddit_name,
                     config.sort_criteria,
                     config.batch_size,
                     config.days_ago,
                     config.limit
                 )

            elif config.type == "search":
                 self.extraction_use_case.extract_posts_from_search(
                    config.query,
                    config.sort_criteria,
                    config.batch_size,
                    config.days_ago,
                    config.limit
                 )
            self.database_adapter.update_extraction_config(config.id)
            logger.info(f"Extração com ID {config.id} finalizada com sucesso.")
        except Exception as e:
            logger.error(f"Erro durante a execução da extração com ID {config.id}: {e}")
        finally:
            time.sleep(self.job_interval)

    def run_extraction_now(self, config):
        """Runs the extraction immediately."""
        logger.info(f"Executando extração manualmente com ID {config.id}")
        run_in_thread(self._execute_extraction, config)

    def shutdown(self):
        """Shuts down the scheduler."""
        self.scheduler.shutdown()
        logger.info("Agendador de extração finalizado.")
```

## src/adapters/saas_ideas_adapter.py
```python
# src/adapters/saas_ideas_adapter.py
from typing import List, Optional, Dict
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, text, DateTime, Boolean, asc, desc
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError
from src.config.config import Config
from src.core.ports.saas_ideas_gateway import SaasIdeasGateway
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


class SaasIdeasAdapter(SaasIdeasGateway):
    def __init__(self):
        self.config = Config()
        url = f"postgresql://{self.config.POSTGRES_USER}:{self.config.POSTGRES_PASSWORD}@{self.config.POSTGRES_HOST}:{self.config.POSTGRES_PORT}/{self.config.POSTGRES_DB}"
        self.engine = create_engine(url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base = declarative_base()

        class SaasIdeaDB(Base):
            __tablename__ = "saas_ideas"

            id = Column(Integer, primary_key=True, autoincrement=True)
            name = Column(String, nullable=False)
            description = Column(String)
            differentiators = Column(JSON)
            features = Column(JSON)
            implementation_score = Column(Integer)
            market_viability_score = Column(Integer)
            category = Column(String)
            post_id = Column(String, ForeignKey("posts.id"))
            post = relationship("PostDB")

        class PostDB(Base):
            __tablename__ = "posts"

            id = Column(String, primary_key=True)
            title = Column(String, nullable=False)
            url = Column(String, nullable=False)
            text = Column(String)
            num_comments = Column(Integer)
            ups = Column(Integer)
            created_at = Column(DateTime)
            gemini_analysis = Column(Boolean, default=False)
            comments = relationship("CommentDB", back_populates="post", cascade="all, delete-orphan")

        class CommentDB(Base):
            __tablename__ = "comments"

            id = Column(Integer, primary_key=True, autoincrement=True)
            author = Column(String)
            text = Column(String)
            created_utc = Column(DateTime)
            ups = Column(Integer)
            post_id = Column(String, ForeignKey("posts.id"))
            post = relationship("PostDB", back_populates="comments")

        self.SaasIdeaDB = SaasIdeaDB
        self.PostDB = PostDB
        self.CommentDB = CommentDB

    def list_saas_ideas(
            self,
            category: Optional[str] = None,
            features: Optional[str] = None,
            differentiators: Optional[str] = None,
            description: Optional[str] = None,
            page: int = 1,
            page_size: int = 10,
            order_by: Optional[str] = None,
            order_direction: Optional[str] = "asc"
    ) -> Dict:
        db = self.SessionLocal()
        try:
            query = db.query(self.SaasIdeaDB)

            if category is not None:
                query = query.filter(self.SaasIdeaDB.category == category)

            if features:
                query = query.filter(self.SaasIdeaDB.features.like(f"%{features}%"))
            if differentiators:
                query = query.filter(self.SaasIdeaDB.differentiators.like(f"%{differentiators}%"))
            if description:
                query = query.filter(self.SaasIdeaDB.description.like(f"%{description}%"))

            if order_by:
                order_by_column = getattr(self.SaasIdeaDB, order_by)
                if order_direction == "asc":
                    query = query.order_by(asc(order_by_column))
                else:
                    query = query.order_by(desc(order_by_column))

            total = query.count()
            saas_ideas = query.offset((page - 1) * page_size).limit(page_size).all()
            return {
                "items": [idea.__dict__ for idea in saas_ideas],
                "total": total,
                "page": page,
                "page_size": page_size,
            }
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar ideias Saas: {e}")
            return {"items": [], "total": 0, "page": page, "page_size": page_size}

        finally:
            db.close()

    def list_all_categories(self) -> List[str]:
        db = self.SessionLocal()
        try:
            categories = db.query(self.SaasIdeaDB.category).distinct().all()
            return [category[0] for category in categories if category[0]]
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar categorias: {e}")
            return []
        finally:
            db.close()
```

## src/adapters/gemini_adapter.py
```python
# src/adapters/gemini_adapter.py
import google.generativeai as genai
import json
import threading
import time
from typing import Dict, Optional

from src.config.config import Config
from src.core.ports.gemini_gateway import GeminiGateway
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


class GeminiAdapter(GeminiGateway):
    def __init__(self):
        self.config = Config()
        try:
            genai.configure(api_key=self.config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(self.config.GEMINI_MODEL)
            logger.info("Conexão com Gemini estabelecida com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao conectar com o Gemini: {e}")
            self.model = None
        self.semaphore = threading.Semaphore(1)  # Limita para 1 thread por vez
        self.retry_delay = 10  # Tempo de espera entre as tentativas em segundos
        self.max_retries = 3  # Número máximo de tentativas

    def analyze_text(self, text: str, post_title: str) -> Optional[Dict]:
        """
        Analisa um texto usando a API do Google Gemini, garantindo um formato de resposta JSON consistente.

        Args:
          text: texto a ser analisado
          post_title: titulo do post para inserir no json de resposta
        Returns:
           Um dicionário contendo o title, description, category e score.
        """
        if not self.model:
            logger.error("Modelo Gemini não está inicializado.")
            return {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}}

        retries = 0
        while retries < self.max_retries:
            prompt = f"""
            You are an assistant specialized in content analysis to identify opportunities for the development of SaaS products. Your task is to analyze a text from a post and its comments, and generate insights about pains, problems, and solutions reported, formatting the response in a specific JSON structure. All your responses must be in english

            Instructions:

            1.  Analyze the text to identify problems or challenges mentioned.
            2.  Identify any proposed solutions or ideas that can be transformed into SaaS products.
            3.  For each SaaS product opportunity identified:
                *   Create a catchy name for the product.
                *   Describe how the product would solve the problem.
                *   List the main differentiators.
                *   List the main features.
                *   Assign an implementation ease score (1 to 5).
                *   Assign a market viability score (1 to 100).
            4.  For each identified SaaS product, categorize it in one of the following categories:
                - Project Management
                - Customer Relationship Management
                - Marketing and Sales Automation
                - Finance Management
                - Human Resources Management
                - E-commerce and Retail
                - Education and Training
                - Data Analytics and Business Intelligence
                - Health and Wellness
                - Social Media Management
                - Productivity and Workflow
                - Collaboration and Communication
                - IT and Security Management
            5.  Format the output as a JSON following the structure:

            {{
                "post_analysis": {{
                    "insights": [
                        {{
                            "problem": "Problem identified in the text",
                            "saas_product": {{
                                "description": "Description of the SaaS product",
                                "differentiators": ["Differentiator 1", "Differentiator 2", ...],
                                "features": ["Feature 1", "Feature 2", ...],
                                "implementation_score": int,
                                "market_viability_score": int,
                                "name": "SaaS Product Name",
                                "category": "Category of the SaaS product"
                            }},
                            "solution": "Proposed solution"
                        }},
                    ... (More opportunities, if found)
                ],
                "post_description": "General post description",
                "post_title": "Post title"
                }}
            }}

            6. If no idea is found, return the structure with empty insights:
            {{
                "post_analysis": {{
                    "insights": [],
                    "post_description": "",
                    "post_title": "Post title"
                }}
            }}


            Here is the text to be analyzed:
            {text}

            Strictly adhere to the JSON structure, without adding any extra fields and without removing any mandatory fields.
            """
            try:
                with self.semaphore:
                    response = self.model.generate_content(prompt)
                    json_str = response.text.replace("```json", "").replace("```", "")
                    response_json = json.loads(json_str)

                    if not response_json.get("post_analysis") or not isinstance(
                            response_json.get("post_analysis").get("insights"), list):
                        logger.warning("Formato da resposta do Gemini está incorreta, retornando insights vazios")
                        return {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}}

                    return response_json
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao decodificar resposta JSON do Gemini: {e}")
                return {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}}
            except Exception as e:
                logger.error(f"Erro ao analisar com Gemini: {e}")
                if "429 Resource has been exhausted" in str(e):
                    retries += 1
                    logger.warning(
                        f"Erro de quota do Gemini, tentando novamente em {self.retry_delay} segundos (tentativa {retries}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                else:
                    return {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}}
        return {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}}
```

## src/adapters/database_adapter.py
```python
# src/adapters/database_adapter.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List, Optional

from src.config.config import Config
from src.core.ports.database_gateway import DatabaseGateway
from src.database.models.database_models import Base, PostDB, CommentDB, SaasIdeaDB, ExtractionConfigDB
from src.core.utils.logger import setup_logger
from src.core.entities import Post, Comment
from sqlalchemy.orm import Session

logger = setup_logger(__name__)


class DatabaseAdapter(DatabaseGateway):
    def __init__(self):
        self.config = Config()
        self.engine = self._create_engine()
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_engine(self):
        """Creates and returns the database engine."""
        try:
            url = f"postgresql://{self.config.POSTGRES_USER}:{self.config.POSTGRES_PASSWORD}@{self.config.POSTGRES_HOST}:{self.config.POSTGRES_PORT}/{self.config.POSTGRES_DB}"
            engine = create_engine(url)
            logger.info("Conexão com o banco de dados estabelecida com sucesso.")
            return engine
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar engine do banco de dados: {e}")
            raise

    def _create_tables(self):
        """Creates database tables if they don't exist."""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Tabelas do banco de dados criadas com sucesso.")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar tabelas do banco de dados: {e}")
            raise

    def add_post(self, post: Post) -> Optional[str]:
        """Adds a post to the database."""
        session = self.Session()
        try:
            if self.post_exists(post.id, session):
                logger.info(f"Post com ID {post.id} já existe no banco de dados. Ignorando.")
                return None

            post_db = PostDB(
                id=post.id,
                title=post.title,
                url=post.url,
                text=post.text,
                num_comments=post.num_comments,
                ups=post.ups,
                created_at=datetime.now(),
            )

            for comment_data in post.comments:
                comment_db = CommentDB(
                    author=comment_data.author,
                    text=comment_data.text,
                    created_utc=comment_data.created_utc,
                    ups=comment_data.ups,
                    post=post_db,
                )
                session.add(comment_db)

            session.add(post_db)
            session.commit()
            logger.info(f"Post com ID {post.id} adicionado ao banco de dados com sucesso.")
            return post_db.id

        except SQLAlchemyError as e:
            logger.error(f"Erro ao adicionar post com ID {post.id} no banco de dados: {e}")
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar post com ID {post.id} no banco de dados: {e}")
            session.rollback()
        finally:
            session.close()

    def add_saas_ideas(self, post_id: str, gemini_analysis: dict) -> None:
        """Adds a saas idea to the database."""
        session = self.Session()
        try:
            post_db = session.query(PostDB).filter_by(id=post_id).first()
            if not post_db:
                logger.warning(f"Post com ID {post_id} não encontrado, impossivel salvar ideias saas.")
                return

            if gemini_analysis and gemini_analysis.get("post_analysis") and gemini_analysis.get("post_analysis").get(
                    "insights"):
                logger.info(f"Salvando ideias de SaaS para post {post_id}")
                for idea_data in gemini_analysis["post_analysis"]["insights"]:
                    if idea_data and idea_data.get("saas_product"):
                        saas_product = idea_data.get("saas_product")
                        saas_idea_db = SaasIdeaDB(
                            name=saas_product.get("name"),
                            description=saas_product.get("description"),
                            differentiators=saas_product.get("differentiators"),
                            features=saas_product.get("features"),
                            implementation_score=saas_product.get("implementation_score"),
                            market_viability_score=saas_product.get("market_viability_score"),
                            category=saas_product.get("category"),
                            post=post_db
                        )
                        session.add(saas_idea_db)
                        logger.info(f"Ideia de SaaS '{saas_product.get('name')}' salva para o post {post_id}")

            else:
                logger.info(f"Não foram encontradas ideias de SaaS para o post {post_id}")

            post_db.gemini_analysis = True
            session.commit()
            logger.info(f"Post com ID {post_id} atualizado como analisado")

        except SQLAlchemyError as e:
            logger.error(f"Erro ao adicionar ideia saas para o post com ID {post_id}: {e}")
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar ideia saas para o post com ID {post_id}: {e}")
            session.rollback()
        finally:
            session.close()

    def post_exists(self, post_id: str, session: Session = None) -> bool:
        """Checks if a post with the given ID already exists in the database."""
        if session is None:
            session = self.Session()
            try:
                return session.query(PostDB).filter_by(id=post_id).first() is not None
            finally:
                session.close()
        else:
            return session.query(PostDB).filter_by(id=post_id).first() is not None

    def post_already_analyzed(self, post_id: str, session: Session = None) -> bool:
        """Checks if a post with the given ID already has gemini analysis"""
        if session is None:
            session = self.Session()
            try:
                post = session.query(PostDB).filter_by(id=post_id).first()
                return post is not None and post.gemini_analysis == True
            finally:
                session.close()
        else:
            post = session.query(PostDB).filter_by(id=post_id).first()
            return post is not None and post.gemini_analysis == True

    def add_extraction_config(self, config_data: dict) -> None:
        """Adds a new extraction config."""
        session = self.Session()
        try:
            config_db = ExtractionConfigDB(**config_data)
            session.add(config_db)
            session.commit()
            logger.info(f"Configuração de extração adicionada com sucesso.")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao adicionar configuração de extração: {e}")
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar configuração de extração: {e}")
            session.rollback()
        finally:
            session.close()

    def get_all_extraction_configs(self) -> List[ExtractionConfigDB]:
        """Gets all extraction configurations from the database."""
        session = self.Session()
        try:
            configs = session.query(ExtractionConfigDB).filter(ExtractionConfigDB.enabled == True).all()
            return configs
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar configurações de extração: {e}")
            return []
        finally:
            session.close()

    def update_extraction_config(self, config_id: int) -> None:
        """Updates the last run time for an extraction config."""
        session = self.Session()
        try:
            config = session.query(ExtractionConfigDB).filter_by(id=config_id).first()
            if config:
                config.last_run = datetime.now()
                session.commit()
                logger.info(f"Configuração de extração com ID {config_id} atualizada com sucesso")
            else:
                logger.warning(f"Configuração de extração com ID {config_id} não encontrada")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar configuração de extração: {e}")
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar configuração de extração: {e}")
            session.rollback()
        finally:
            session.close()

    def update_post_analysis(self, post_id: str) -> None:
        """Updates the post gemini_analysis to true"""
        session = self.Session()
        try:
            post = session.query(PostDB).filter_by(id=post_id).first()
            if post:
                post.gemini_analysis = True
                session.commit()
                logger.info(f"Post com ID {post_id} atualizado como analisado")
            else:
                logger.warning(f"Post com ID {post_id} não encontrado")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar post com ID {post_id}: {e}")
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar post com ID {post_id}: {e}")
            session.rollback()
        finally:
            session.close()

    def get_posts_to_analyze(self, batch_size: int = 10) -> List[Post]:
        """Gets posts that are not analyzed"""
        session = self.Session()
        try:
            offset = 0
            posts_to_analyze = []
            while True:
                posts = session.query(PostDB).filter(PostDB.gemini_analysis == False).limit(batch_size).offset(
                    offset).all()
                if not posts:
                    logger.info("Não há mais posts para analisar.")
                    break
                posts_to_analyze.extend([
                    Post(
                        title=post.title,
                        id=post.id,
                        url=post.url,
                        text=post.text,
                        num_comments=post.num_comments,
                        ups=post.ups,
                        comments=[
                            Comment(
                                author=comment.author,
                                text=comment.text,
                                created_utc=comment.created_utc,
                                ups=comment.ups
                            ) for comment in post.comments
                        ]) for post in posts
                ])
                offset += batch_size
            return posts_to_analyze
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar posts para análise: {e}")
            return []
        finally:
            session.close()
```

## src/adapters/reddit_adapter.py
```python
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

```

## src/adapters/__pycache__/database_adapter.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/adapters/__pycache__/reddit_adapter.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/adapters/__pycache__/extraction_scheduler.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/adapters/__pycache__/__init__.cpython-311.pyc
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
```

## src/adapters/api/__init__.py
```python

```

## src/adapters/api/main.py
```python
# src/adapters/api/main.py
from typing import List, Optional, Dict
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from src.config.config import Config
from src.core.ports.saas_ideas_gateway import SaasIdeasGateway
from src.adapters.saas_ideas_adapter import SaasIdeasAdapter
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)

class SaasIdea(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    differentiators: Optional[List[str]] = None
    features: Optional[List[str]] = None
    implementation_score: Optional[int] = None
    market_viability_score: Optional[int] = None
    category: Optional[str] = None
    post_id: str
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: List[SaasIdea]
    total: int
    page: int
    page_size: int

app = FastAPI()

origins = [
    "http://localhost:3000", #  Seu frontend
    "https://ideaforge.bemysaas.com.br"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_saas_ideas_adapter():
    adapter = SaasIdeasAdapter()
    return adapter


@app.get("/saas_ideas", response_model=PaginatedResponse)
def list_saas_ideas(
    category: Optional[str] = Query(None),
    features: Optional[str] = Query(None),
    differentiators: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0),
    order_by: Optional[str] = Query(None, enum=["implementation_score", "market_viability_score", "category"]),
    order_direction: Optional[str] = Query("asc", enum=["asc", "desc"]),
    saas_ideas_gateway: SaasIdeasGateway = Depends(get_saas_ideas_adapter)
):
    try:
        saas_ideas = saas_ideas_gateway.list_saas_ideas(
            category=category,
            features=features,
            differentiators=differentiators,
            description=description,
            page=page,
            page_size=page_size,
            order_by=order_by,
            order_direction=order_direction
        )
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar ideias Saas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar ideias Saas no banco de dados")

    if not saas_ideas["items"]:
        raise HTTPException(status_code=404, detail="Nenhuma ideia SaaS encontrada com os filtros fornecidos.")

    return saas_ideas

@app.get("/saas_categories", response_model=List[str])
def list_saas_categories(
    saas_ideas_gateway: SaasIdeasGateway = Depends(get_saas_ideas_adapter)
):
    try:
        categories = saas_ideas_gateway.list_all_categories()
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar categorias Saas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar categorias Saas no banco de dados")

    if not categories:
        raise HTTPException(status_code=404, detail="Nenhuma categoria SaaS encontrada.")

    return categories
```


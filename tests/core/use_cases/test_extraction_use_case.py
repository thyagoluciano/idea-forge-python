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
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
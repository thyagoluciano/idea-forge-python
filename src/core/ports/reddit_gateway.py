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
    
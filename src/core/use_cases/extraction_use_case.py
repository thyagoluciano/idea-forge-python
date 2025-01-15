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

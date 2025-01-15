# src/adapters/database_adapter.py
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from src.core.ports.database_gateway import DatabaseGateway
from src.database.database_manager import DatabaseManager
from src.database.repositories.post_repository import PostRepository
from src.database.repositories.saas_idea_repository import SaasIdeaRepository
from src.database.repositories.extraction_config_repository import ExtractionConfigRepository
from src.core.utils.logger import setup_logger
from src.core.entities import Post, Comment
from src.database.models.post_db import PostDB

logger = setup_logger(__name__)


class DatabaseAdapter(DatabaseGateway):
    def __init__(self):
        self.database_manager = DatabaseManager()
        self.post_repository = PostRepository(self.database_manager)
        self.saas_idea_repository = SaasIdeaRepository(self.database_manager)
        self.extraction_config_repository = ExtractionConfigRepository(self.database_manager)

    def add_post(self, post: Post) -> Optional[str]:
        """Adds a post to the database."""
        return self.post_repository.add_post(post)

    def add_saas_ideas(self, post_id: str, gemini_analysis: dict) -> None:
        """Adds a saas idea to the database."""
        self.saas_idea_repository.add_saas_ideas(post_id, gemini_analysis)

    def post_exists(self, post_id: str) -> bool:
       """Checks if a post with the given ID already exists in the database."""
       with self.database_manager.session() as session:
           return self.post_repository.post_exists(post_id, session)

    def post_already_analyzed(self, post_id: str) -> bool:
        """Checks if a post with the given ID already has gemini analysis"""
        with self.database_manager.session() as session:
            return self.post_repository.post_already_analyzed(post_id, session)

    def add_extraction_config(self, config_data: dict) -> None:
        """Adds a new extraction config."""
        self.extraction_config_repository.add_extraction_config(config_data)

    def get_all_extraction_configs(self) -> List[dict]:
       """Gets all extraction configurations from the database."""
       return self.extraction_config_repository.get_all_extraction_configs()

    def update_extraction_config(self, config_id: int) -> None:
       """Updates the last run time for an extraction config."""
       self.extraction_config_repository.update_extraction_config(config_id)

    def update_post_analysis(self, post_id: str) -> None:
        """Updates the post gemini_analysis to true"""
        self.post_repository.update_post_analysis(post_id)

    def get_posts_to_analyze(self, batch_size: int = 10) -> List[Post]:
        """Gets posts that are not analyzed"""
        try:
            with self.database_manager.session() as session:
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
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar posts para análise: {e}")
            return []
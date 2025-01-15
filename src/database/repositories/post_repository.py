# src/database/repositories/post_repository.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from src.database.models.database_models import PostDB, CommentDB
from src.core.entities import Post
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


class PostRepository:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def add_post(self, post: Post) -> Optional[str]:
        """Adds a post to the database."""
        try:
            with self.database_manager.session() as session:
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
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar post com ID {post.id} no banco de dados: {e}")
            return None

    def post_exists(self, post_id: str, session: Session) -> bool:
        """Checks if a post with the given ID already exists in the database."""
        return session.query(PostDB).filter_by(id=post_id).first() is not None

    def post_already_analyzed(self, post_id: str, session: Session) -> bool:
        """Checks if a post with the given ID already has gemini analysis"""
        post = session.query(PostDB).filter_by(id=post_id).first()
        return post is not None and post.gemini_analysis == True

    def update_post_analysis(self, post_id: str) -> None:
        """Updates the post gemini_analysis to true"""
        try:
            with self.database_manager.session() as session:
                post = session.query(PostDB).filter_by(id=post_id).first()
                if post:
                    post.gemini_analysis = True
                    session.commit()
                    logger.info(f"Post com ID {post_id} atualizado como analisado")
                else:
                    logger.warning(f"Post com ID {post_id} não encontrado")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar post com ID {post_id}: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar post com ID {post_id}: {e}")

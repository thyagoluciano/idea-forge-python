from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.config.config import Config
from src.models.database_models import Base, PostDB, CommentDB
from src.utils.logger import logger


class DatabaseManager:
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

    def add_post(self, post_data):
        """Adds a post to the database."""
        session = self.Session()
        try:
            if self.post_exists(post_data.id, session):
                logger.info(f"Post com ID {post_data.id} já existe no banco de dados. Ignorando.")
                return

            post_db = PostDB(
                id=post_data.id,
                title=post_data.title,
                url=post_data.url,
                text=post_data.text,
                num_comments=post_data.num_comments,
                ups=post_data.ups,
                created_at=datetime.now(),
            )

            for comment_data in post_data.comments:
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
            logger.info(f"Post com ID {post_data.id} adicionado ao banco de dados com sucesso.")

        except SQLAlchemyError as e:
            logger.error(f"Erro ao adicionar post com ID {post_data.id} no banco de dados: {e}")
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar post com ID {post_data.id} no banco de dados: {e}")
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def post_exists(post_id, session):
        """Checks if a post with the given ID already exists in the database."""
        return session.query(PostDB).filter_by(id=post_id).first() is not None
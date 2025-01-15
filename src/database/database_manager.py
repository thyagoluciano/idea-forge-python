# src/database/database_manager.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.config.config import Config
from src.database.models.database_models import Base
from src.core.utils.logger import setup_logger
from contextlib import contextmanager

logger = setup_logger(__name__)


class DatabaseManager:
    def __init__(self):
        self.config = Config()
        self.engine = self._create_engine()
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

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

    @contextmanager
    def session(self):
        """Context manager for database sessions."""
        session = self.Session()
        try:
            yield session
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro na sessão do banco de dados: {e}")
            raise
        finally:
            session.close()
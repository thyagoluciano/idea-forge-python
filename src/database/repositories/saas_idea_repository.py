from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.database.models.saas_idea_db import SaasIdeaDB
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


class SaasIdeaRepository:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def add_saas_idea(self, saas_idea: SaasIdeaDB) -> None:
        """Adds a saas idea to the database."""
        try:
            with self.database_manager.session() as session:
                if self.saas_idea_exists(saas_idea.id, session):
                    logger.info(
                        f"Ideia SaaS com ID {saas_idea.id} já existe no banco de dados. Ignorando.")
                    return
                session.add(saas_idea)
                session.commit()
                logger.info(f"Ideia de SaaS '{saas_idea.name}' salva para o post {saas_idea.post_id}")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao adicionar ideia saas para o post com ID {saas_idea.post_id}: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar ideia saas para o post com ID {saas_idea.post_id}: {e}")

    @staticmethod
    def saas_idea_exists(saas_idea_id: int, session: Session) -> bool:
        """Checks if a saas idea with the given ID already exists in the database."""
        return session.query(SaasIdeaDB).filter_by(id=saas_idea_id).first() is not None

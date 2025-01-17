from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.utils.logger import setup_logger
from src.database.models.saas_idea_pt_db import SaasIdeaPtDB

logger = setup_logger(__name__)


class SaasIdeaPtRepository:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def add_saas_idea_pt(self, saas_idea_pt: SaasIdeaPtDB) -> Optional[int]:
        """Adds a saas idea to the database."""
        try:
            with self.database_manager.session() as session:
                if self.saas_idea_pt_exists(saas_idea_pt.id, session):
                    logger.info(
                        f"Ideia SaaS com ID {saas_idea_pt.id} já existe no banco de dados. Ignorando.")
                    return
                session.add(saas_idea_pt)
                session.commit()
                logger.info(f"Ideia de SaaS '{saas_idea_pt.name}' salva para o post {saas_idea_pt.post_id}")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao adicionar ideia saas para o post com ID {saas_idea_pt.post_id}: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar ideia saas para o post com ID {saas_idea_pt.post_id}: {e}")

    @staticmethod
    def saas_idea_pt_exists(saas_idea_id: int, session: Session) -> bool:
        """Checks if a translated saas idea with the given original ID already exists in the database."""
        return session.query(SaasIdeaPtDB).filter_by(id=saas_idea_id).first() is not None

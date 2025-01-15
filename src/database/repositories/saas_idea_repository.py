# src/database/repositories/saas_idea_repository.py
from sqlalchemy.exc import SQLAlchemyError

from src.database.models.saas_idea_db import SaasIdeaDB
from src.database.models.post_db import PostDB
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


class SaasIdeaRepository:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def add_saas_ideas(self, post_id: str, gemini_analysis: dict) -> None:
        """Adds a saas idea to the database."""
        try:
            with self.database_manager.session() as session:
                post_db = session.query(PostDB).filter_by(id=post_id).first()
                if not post_db:
                     logger.warning(f"Post com ID {post_id} não encontrado, impossivel salvar ideias saas.")
                     return
                if gemini_analysis and gemini_analysis.get("post_analysis") and gemini_analysis.get("post_analysis").get(
                         "insights"):
                    logger.info(f"Salvando ideias de SaaS para post {post_id}")
                    for idea_data in gemini_analysis["post_analysis"]["insights"]:
                        if idea_data and idea_data.get("saas_product"):
                            saas_product = idea_data.get("saas_product")
                            saas_idea_db = SaasIdeaDB(
                                name=saas_product.get("name"),
                                description=saas_product.get("description"),
                                differentiators=saas_product.get("differentiators"),
                                features=saas_product.get("features"),
                                implementation_score=saas_product.get("implementation_score"),
                                market_viability_score=saas_product.get("market_viability_score"),
                                category=saas_product.get("category"),
                                post=post_db
                             )
                            session.add(saas_idea_db)
                            logger.info(f"Ideia de SaaS '{saas_product.get('name')}' salva para o post {post_id}")

                else:
                     logger.info(f"Não foram encontradas ideias de SaaS para o post {post_id}")
                post_db.gemini_analysis = True
                session.commit()
                logger.info(f"Post com ID {post_id} atualizado como analisado")

        except SQLAlchemyError as e:
            logger.error(f"Erro ao adicionar ideia saas para o post com ID {post_id}: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar ideia saas para o post com ID {post_id}: {e}")
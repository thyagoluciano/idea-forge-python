# src/database/repositories/extraction_config_repository.py
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from src.core.utils.logger import setup_logger
from src.database.models.extraction_config_db import ExtractionConfigDB

logger = setup_logger(__name__)


class ExtractionConfigRepository:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def add_extraction_config(self, config_data: dict) -> None:
        """Adds a new extraction config."""
        try:
            with self.database_manager.session() as session:
                config_db = ExtractionConfigDB(**config_data)
                session.add(config_db)
                session.commit()
                logger.info(f"Configuração de extração adicionada com sucesso.")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao adicionar configuração de extração: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar configuração de extração: {e}")

    def get_all_extraction_configs(self) -> List[ExtractionConfigDB]:
        """Gets all extraction configurations from the database."""
        try:
            with self.database_manager.session() as session:
                configs = session.query(ExtractionConfigDB).filter(ExtractionConfigDB.enabled == True).all()
                return configs
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar configurações de extração: {e}")
            return []

    def update_extraction_config(self, config_id: int) -> None:
        """Updates the last run time for an extraction config."""
        try:
            with self.database_manager.session() as session:
                config = session.query(ExtractionConfigDB).filter_by(id=config_id).first()
                if config:
                    config.last_run = datetime.now()
                    session.commit()
                    logger.info(f"Configuração de extração com ID {config_id} atualizada com sucesso")
                else:
                    logger.warning(f"Configuração de extração com ID {config_id} não encontrada")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar configuração de extração: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar configuração de extração: {e}")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from old.config.config import Config
from old.models.database_models import Base, PostDB, CommentDB, SaasIdeaDB, ExtractionConfigDB
from old.utils.logger import logger


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
            return post_db.id

        except SQLAlchemyError as e:
            logger.error(f"Erro ao adicionar post com ID {post_data.id} no banco de dados: {e}")
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar post com ID {post_data.id} no banco de dados: {e}")
            session.rollback()
        finally:
            session.close()

    def add_saas_ideas(self, post_id, gemini_analysis):
        """Adds a saas idea to the database."""
        session = self.Session()
        try:
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
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar ideia saas para o post com ID {post_id}: {e}")
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def post_exists(post_id, session):
        """Checks if a post with the given ID already exists in the database."""
        return session.query(PostDB).filter_by(id=post_id).first() is not None

    @staticmethod
    def post_already_analyzed(post_id, session):
        """Checks if a post with the given ID already has gemini analysis"""
        post = session.query(PostDB).filter_by(id=post_id).first()
        return post is not None and post.gemini_analysis == True

    def add_extraction_config(self, config_data):
        """Adds a new extraction config."""
        session = self.Session()
        try:
            config_db = ExtractionConfigDB(**config_data)
            session.add(config_db)
            session.commit()
            logger.info(f"Configuração de extração adicionada com sucesso.")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao adicionar configuração de extração: {e}")
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar configuração de extração: {e}")
            session.rollback()
        finally:
            session.close()

    def get_all_extraction_configs(self):
        """Gets all extraction configurations from the database."""
        session = self.Session()
        try:
            configs = session.query(ExtractionConfigDB).filter(ExtractionConfigDB.enabled == True).all()
            return configs
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar configurações de extração: {e}")
            return []
        finally:
            session.close()

    def update_extraction_config(self, config_id):
        """Updates the last run time for an extraction config."""
        session = self.Session()
        try:
            config = session.query(ExtractionConfigDB).filter_by(id=config_id).first()
            if config:
                config.last_run = datetime.now()
                session.commit()
                logger.info(f"Configuração de extração com ID {config_id} atualizada com sucesso")
            else:
                logger.warning(f"Configuração de extração com ID {config_id} não encontrada")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar configuração de extração: {e}")
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar configuração de extração: {e}")
            session.rollback()
        finally:
            session.close()

    def update_post_analysis(self, post_id):
        """Updates the post gemini_analysis to true"""
        session = self.Session()
        try:
            post = session.query(PostDB).filter_by(id=post_id).first()
            if post:
                post.gemini_analysis = True
                session.commit()
                logger.info(f"Post com ID {post_id} atualizado como analisado")
            else:
                logger.warning(f"Post com ID {post_id} não encontrado")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar post com ID {post_id}: {e}")
            session.rollback()
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar post com ID {post_id}: {e}")
            session.rollback()
        finally:
            session.close()
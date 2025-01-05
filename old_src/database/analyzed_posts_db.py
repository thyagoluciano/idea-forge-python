from old_src.database.postgres_database import PostgresDatabase
from psycopg2 import Error
from old_src.utils.logger import logger
import traceback

class AnalyzedPostsDB(PostgresDatabase):
    def __init__(self, connection=None):
        super().__init__()
        self.connection = connection if connection else self.connection
        self._setup_database()

    def _setup_database(self):
        """Verifica e cria a tabela analyzed_posts, se necessário."""
        if not self.connection:
            return

        try:
            with self.connection.cursor() as cursor:
                # Cria tabela analyzed_posts, se não existir
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analyzed_posts (
                        id SERIAL PRIMARY KEY,
                        reddit_post_id VARCHAR(255) NOT NULL UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            self.connection.commit()
            logger.info("Tabela 'analyzed_posts' verificada e criada, se necessário.")
        except Error as e:
            logger.error(f"Erro ao verificar/criar tabela 'analyzed_posts': {e}")


    def add_analyzed_post(self, reddit_post_id):
        """Adiciona um ID de post analisado ao banco de dados."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para adicionar posts analisados.")
            return False
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO analyzed_posts (reddit_post_id) VALUES (%s)",
                    (reddit_post_id,),
                )
                self.connection.commit()
                logger.debug(f"Post com ID {reddit_post_id} adicionado aos posts analisados.")
                return True
        except Error as e:
            logger.error(f"Erro ao adicionar post analisado: {e}")
            logger.error(traceback.format_exc())
            self.connection.rollback()
            return False


    def is_duplicate_post(self, reddit_post_id):
        """Verifica se um post já foi analisado."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para verificar duplicidades de posts analisados.")
            return False
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT EXISTS(SELECT 1 FROM analyzed_posts WHERE reddit_post_id = %s)",
                    (reddit_post_id,),
                )
                return cursor.fetchone()[0]
        except Error as e:
            logger.error(f"Erro ao verificar duplicidade de post analisado: {e}")
            return False
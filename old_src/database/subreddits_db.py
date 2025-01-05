from old_src.database.postgres_database import PostgresDatabase
from psycopg2 import Error
from old_src.utils.logger import logger


class SubredditsDB(PostgresDatabase):
    def __init__(self, connection = None):
        super().__init__()
        self.connection = connection if connection else self.connection
        self._setup_database()

    def _setup_database(self):
        """Verifica e cria a tabela subreddits, se necessário."""
        if not self.connection:
            return

        try:
            with self.connection.cursor() as cursor:
                # Cria tabela subreddits, se não existir
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS subreddits (
                        id SERIAL PRIMARY KEY,
                        subreddit_name VARCHAR(255) NOT NULL UNIQUE,
                        sort_type VARCHAR(255) NOT NULL DEFAULT 'hot',
                        limit_posts INTEGER NOT NULL DEFAULT 10,
                        last_extraction_date TIMESTAMP,
                        next_extraction_date TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            self.connection.commit()
            logger.info("Tabela 'subreddits' verificada e criada, se necessário.")
        except Error as e:
            logger.error(f"Erro ao verificar/criar tabela 'subreddits': {e}")

    def add_subreddit(self, subreddit_name, sort_type='hot', limit_posts=10):
        """Adiciona um novo subreddit à tabela subreddits."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para adicionar subreddits.")
            return False
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO subreddits (subreddit_name, sort_type, limit_posts)
                    VALUES (%s, %s, %s)
                """,
                (subreddit_name, sort_type, limit_posts),
                )
                self.connection.commit()
                logger.info(f"Subreddit '{subreddit_name}' adicionado ao banco de dados.")
                return True
        except Error as e:
            logger.error(f"Erro ao adicionar subreddit: {e}")
            return False

    def get_all_subreddits(self):
        """Retorna todos os subreddits da tabela subreddits."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para buscar os subreddits.")
            return []
        try:
             with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM subreddits")
                subreddits = cursor.fetchall()
                return subreddits
        except Error as e:
            logger.error(f"Erro ao buscar subreddits no banco de dados: {e}")
            return []

    def get_subreddits_to_extract(self):
            """Retorna o proximo subreddit que tem a data de next_extraction_date menor ou igual a data atual."""
            if not self.connection:
                logger.error("Não há conexão com o banco de dados para buscar os subreddits.")
                return []
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM subreddits WHERE next_extraction_date <= NOW() OR next_extraction_date IS NULL LIMIT 1")
                    subreddit = cursor.fetchone()
                    return [subreddit] if subreddit else []
            except Error as e:
                logger.error(f"Erro ao buscar subreddits no banco de dados: {e}")
                return []

    def update_subreddit_extraction_date(self, subreddit_id):
        """Atualiza as datas de last_extraction_date e next_extraction_date para um subreddit específico."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para atualizar as datas de extração do subreddit.")
            return False
        try:
              with self.connection.cursor() as cursor:
                  cursor.execute(
                    """
                    UPDATE subreddits
                    SET last_extraction_date = NOW(),
                        next_extraction_date = NOW() + INTERVAL '7 days'
                    WHERE id = %s
                    """,
                    (subreddit_id,),
                   )
                  self.connection.commit()
                  logger.info(f"Datas de extração do subreddit com ID '{subreddit_id}' atualizadas com sucesso.")
                  return True
        except Error as e:
                logger.error(f"Erro ao atualizar as datas de extração do subreddit: {e}")
                return False
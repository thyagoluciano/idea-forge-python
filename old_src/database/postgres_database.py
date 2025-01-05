import psycopg2
from psycopg2 import Error
from old_src.config.config import Config
from old_src.utils.logger import logger


class PostgresDatabase:
    def __init__(self):
        self.config = Config()
        self.connection = self._connect()

    def _connect(self):
        """Estabelece conexão com o banco de dados PostgreSQL."""
        try:
            conn = psycopg2.connect(
                host=self.config.POSTGRES_HOST,
                port=self.config.POSTGRES_PORT,
                user=self.config.POSTGRES_USER,
                password=self.config.POSTGRES_PASSWORD,
                database=self.config.POSTGRES_DB
            )
            logger.info("Conexão com PostgreSQL estabelecida com sucesso.")
            return conn
        except Error as e:
            logger.error(f"Erro ao conectar com o PostgreSQL: {e}")
            return None

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()
            logger.info("Conexão com o banco de dados fechada.")
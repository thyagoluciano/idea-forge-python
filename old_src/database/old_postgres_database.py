import psycopg2
from psycopg2 import Error
from old_src.config.config import Config
from old_src.models.idea import Idea
from old_src.utils.logger import logger


class PostgresDatabase:
    def __init__(self):
        self.config = Config()
        self.connection = self._connect()
        self._setup_database()

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

    def _setup_database(self):
        """Verifica e cria tabelas, se necessário."""
        if not self.connection:
            return

        try:
            with self.connection.cursor() as cursor:
                # Cria tabela ideas, se não existir
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ideas (
                        id SERIAL PRIMARY KEY,
                        reddit_content_id VARCHAR(255) NOT NULL,
                        product_name VARCHAR(255),
                        problem TEXT,
                        solution_description TEXT,
                        implementation_score INTEGER,
                        market_viability_score INTEGER,
                        differentials TEXT,
                        features TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(reddit_content_id, product_name)
                    );
                """)
                # Cria tabela analyzed_posts, se não existir
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analyzed_posts (
                        id SERIAL PRIMARY KEY,
                        reddit_post_id VARCHAR(255) NOT NULL UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            self.connection.commit()
            logger.info("Tabelas 'ideas' e 'analyzed_posts' verificadas e criadas, se necessário.")
        except Error as e:
            logger.error(f"Erro ao verificar/criar tabelas: {e}")

    def add_idea(self, idea):
        """Adiciona uma nova ideia ao banco de dados."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para adicionar ideias.")
            return False
        if self.is_duplicate_idea(idea):
            logger.warning(f"A ideia com ID {idea.reddit_content_id} e nome '{idea.product_name}' já existe no banco de dados.")
            return False

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ideas (reddit_content_id, product_name, problem, solution_description, implementation_score, market_viability_score, differentials, features)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    idea.reddit_content_id,
                    idea.product_name,
                    idea.problem,
                    idea.solution_description,
                    idea.implementation_score,
                    idea.market_viability_score,
                    idea.differentials,
                    idea.features,
                ),
            )
            self.connection.commit()
            logger.info(f"Ideia '{idea.product_name}' adicionada ao banco de dados.")
            return True
        except Error as e:
            logger.error(f"Erro ao adicionar ideia: {e}")
            return False

    def is_duplicate_idea(self, idea):
        """Verifica se uma ideia já existe no banco de dados."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para verificar duplicidades de ideias.")
            return False
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT EXISTS(SELECT 1 FROM ideas WHERE reddit_content_id = %s AND product_name = %s)",
                    (idea.reddit_content_id, idea.product_name),
                )
                return cursor.fetchone()[0]
        except Error as e:
            logger.error(f"Erro ao verificar duplicidade de ideia: {e}")
            return False

    def get_all_ideas(self):
        """Retorna todas as ideias do banco de dados."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para buscar as ideias.")
            return []
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM ideas")
                ideas_data = cursor.fetchall()
                ideas = [
                    Idea(
                        reddit_content_id=item[1],
                        product_name=item[2],
                        problem=item[3],
                        solution_description=item[4],
                        implementation_score=item[5],
                        market_viability_score=item[6],
                        differentials=item[7],
                        features=item[8],
                    )
                    for item in ideas_data
                ]
                return ideas
        except Error as e:
            logger.error(f"Erro ao buscar ideias no banco de dados: {e}")
            return []

    def add_analyzed_post(self, reddit_post_id):
        """Adiciona um ID de post analisado ao banco de dados."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para adicionar posts analisados.")
            return False
        if self.is_duplicate_post(reddit_post_id):
            logger.warning(f"O post com ID {reddit_post_id} já foi analisado.")
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

    def get_analyzed_post_ids(self):
        """Retorna uma lista com todos os IDs de posts já analisados."""
        if not self.connection:
             logger.error("Não há conexão com o banco de dados para buscar os ids de posts analisados.")
             return []
        try:
            with self.connection.cursor() as cursor:
               cursor.execute("SELECT reddit_post_id FROM analyzed_posts")
               post_ids = [item[0] for item in cursor.fetchall()]
               return post_ids
        except Error as e:
           logger.error(f"Erro ao buscar os ids de posts analisados no banco de dados: {e}")
           return []


    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()
            logger.info("Conexão com o banco de dados fechada.")
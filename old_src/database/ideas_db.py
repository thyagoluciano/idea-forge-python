from old_src.database.postgres_database import PostgresDatabase
from psycopg2 import Error
from old_src.utils.logger import logger
from old_src.models.idea import Idea


class IdeasDB(PostgresDatabase):
    def __init__(self, connection = None):
        super().__init__()
        self.connection = connection if connection else self.connection
        self._setup_database()

    def _setup_database(self):
        """Verifica e cria a tabela ideas, se necessário."""
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
            self.connection.commit()
            logger.info("Tabela 'ideas' verificada e criada, se necessário.")
        except Error as e:
            logger.error(f"Erro ao verificar/criar tabela 'ideas': {e}")

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
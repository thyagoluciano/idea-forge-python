from database.postgres_database import PostgresDatabase
from psycopg2 import Error
from utils.logger import logger


class PostsDB(PostgresDatabase):
    def __init__(self, connection = None):
        super().__init__()
        self.connection = connection if connection else self.connection
        self._setup_database()

    def _setup_database(self):
         """Verifica e cria a tabela reddit_content, se necessário."""
         if not self.connection:
            return

         try:
            with self.connection.cursor() as cursor:
               # Cria tabela reddit_content, se não existir
               cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reddit_content (
                    id SERIAL PRIMARY KEY,
                    subreddit_id INTEGER NOT NULL,
                    post_id VARCHAR(255) NOT NULL UNIQUE,
                    combined_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (subreddit_id) REFERENCES subreddits(id)
                    );
                """)
            self.connection.commit()
            logger.info("Tabela 'reddit_content' verificada e criada, se necessário.")
         except Error as e:
            logger.error(f"Erro ao verificar/criar tabela 'reddit_content': {e}")

    def add_reddit_post(self, subreddit_id, post_id, combined_text):
        """Adiciona um novo post na tabela reddit_content."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para adicionar posts.")
            return False
        try:
             with self.connection.cursor() as cursor:
                 cursor.execute(
                    """
                     INSERT INTO reddit_content (subreddit_id, post_id, combined_text)
                     VALUES (%s, %s, %s)
                     ON CONFLICT (post_id) DO NOTHING
                    """,
                   (subreddit_id, post_id, combined_text),
                  )
                 self.connection.commit()
                 logger.debug(f"Post com ID '{post_id}' adicionado ao banco de dados.")
                 return True
        except Error as e:
            logger.error(f"Erro ao adicionar post: {e}")
            return False

    def delete_reddit_post(self, post_id):
        """Deleta um post da tabela reddit_content."""
        if not self.connection:
            logger.error("Não há conexão com o banco de dados para deletar posts.")
            return False
        try:
             with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM reddit_content WHERE post_id = %s
                     """,
                     (post_id,),
                 )
                self.connection.commit()
                logger.debug(f"Post com ID '{post_id}' deletado do banco de dados.")
                return True
        except Error as e:
            logger.error(f"Erro ao deletar post: {e}")
            return False
    def get_next_reddit_post(self):
      """Retorna o proximo post da tabela reddit_content."""
      if not self.connection:
            logger.error("Não há conexão com o banco de dados para buscar posts.")
            return None
      try:
          with self.connection.cursor() as cursor:
              cursor.execute("SELECT * FROM reddit_content LIMIT 1")
              post = cursor.fetchone()
              return post
      except Error as e:
            logger.error(f"Erro ao buscar posts no banco de dados: {e}")
            return None


    def get_all_reddit_posts(self):
            """Retorna todos os posts da tabela reddit_content."""
            if not self.connection:
                logger.error("Não há conexão com o banco de dados para buscar posts.")
                return []
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM reddit_content")
                    posts = cursor.fetchall()
                    return posts
            except Error as e:
                logger.error(f"Erro ao buscar posts no banco de dados: {e}")
                return []
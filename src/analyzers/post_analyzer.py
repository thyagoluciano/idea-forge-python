from src.core.gemini_api import GeminiAPI
from src.database.database_manager import DatabaseManager
from src.models.database_models import PostDB
from src.utils.logger import logger
import time


class PostAnalyzer:
    def __init__(self):
        self.gemini_api = GeminiAPI()
        self.database_manager = DatabaseManager()
        self.batch_size = 10  # Tamanho do lote
        self.batch_interval = 20  # Intervalo entre os lotes em segundos

    def analyze_posts(self):
        session = self.database_manager.Session()
        try:
            offset = 0
            while True:
                posts = session.query(PostDB).filter(PostDB.gemini_analysis == False).limit(self.batch_size).offset(
                    offset).all()

                if not posts:
                    logger.info("Não há mais posts para analisar.")
                    break

                logger.info(f"Analisando lote de {len(posts)} posts. Offset: {offset}")
                for post in posts:
                    try:
                        self.analyze_post(post)
                    except Exception as e:
                        logger.error(f"Erro ao analisar post {post.id}: {e}")

                offset += self.batch_size
                time.sleep(self.batch_interval)
                logger.info(f"Intervalo de {self.batch_interval} segundos entre os lotes")

        except Exception as e:
            logger.error(f"Erro ao analisar os posts: {e}")
        finally:
            session.close()

    def analyze_post(self, post):
        text_to_analyze = f"{post.title} \n {post.text} \n {' '.join([comment.text for comment in post.comments])}"
        gemini_analysis = self.gemini_api.analyze_with_gemini(text_to_analyze, post.title)
        self.database_manager.add_saas_ideas(post.id, gemini_analysis)
        self.database_manager.update_post_analysis(post.id)
        print(f"Post {post.id} analyzed")

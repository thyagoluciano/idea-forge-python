# src/core/use_cases/analysis_use_case.py
from src.core.ports.gemini_gateway import GeminiGateway
from src.core.ports.database_gateway import DatabaseGateway
from src.core.entities import Post
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


class AnalysisUseCase:
    def __init__(self, gemini_gateway: GeminiGateway, database_gateway: DatabaseGateway):
        self.gemini_gateway = gemini_gateway
        self.database_gateway = database_gateway

    def analyze_posts(self, batch_size: int = 10):
        offset = 0
        while True:
            posts = self.database_gateway.get_posts_to_analyze(batch_size)
            if not posts:
                logger.info("Não há mais posts para analisar.")
                break

            logger.info(f"Analisando lote de {len(posts)} posts. Offset: {offset}")
            for post in posts:
                try:
                    self._analyze_post(post)
                except Exception as e:
                    logger.error(f"Erro ao analisar post {post.id}: {e}")
            offset += batch_size

    def _analyze_post(self, post: Post):
        text_to_analyze = f"{post.title} \n {post.text} \n {' '.join([comment.text for comment in post.comments])}"
        gemini_analysis = self.gemini_gateway.analyze_text(text_to_analyze, post.title)
        self.database_gateway.add_saas_ideas(post.id, gemini_analysis)
        self.database_gateway.update_post_analysis(post.id)
        logger.info(f"Post {post.id} analyzed")
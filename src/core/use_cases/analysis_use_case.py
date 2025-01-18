import time

from src.config.config import Config
from src.core.ports.gemini_gateway import GeminiGateway
from src.core.ports.database_gateway import DatabaseGateway
from src.core.entities import Post
from src.core.utils.logger import setup_logger
from src.database.models.saas_idea_db import SaasIdeaDB
from src.database.models.saas_idea_pt_db import SaasIdeaPtDB

logger = setup_logger(__name__)


class AnalysisUseCase:
    def __init__(self, gemini_gateway: GeminiGateway, database_gateway: DatabaseGateway):
        self.gemini_gateway = gemini_gateway
        self.database_gateway = database_gateway
        self.config = Config()
        self.batch_size = self.config.ANALYSIS_BATCH_SIZE
        self.batch_interval = self.config.ANALYSIS_BATCH_INTERVAL

    def analyze_posts(self):
        offset = 0
        while True:

            posts = self.database_gateway.get_posts_to_analyze(self.batch_size)
            if not posts:
                logger.info("Não há mais posts para analisar.")
                break

            logger.info(f"Analisando lote de {len(posts)} posts. Offset: {offset}")
            for post in posts:
                try:
                    self._analyze_post(post)
                except Exception as e:
                    logger.error(f"Erro ao analisar post {post.id}: {e}")
            offset += self.batch_size
            time.sleep(self.batch_interval)

    def _analyze_post(self, post: Post):
        text_to_analyze = f"{post.title} \n {post.text} \n {' '.join([comment.text for comment in post.comments])}"
        gemini_analysis = self.gemini_gateway.analyze_text(text_to_analyze, post.title)
        if gemini_analysis:
            if gemini_analysis.get("en"):
                self._save_saas_ideas(post.id, gemini_analysis.get("en").get("post_analysis"), "en")
            else:
                logger.warning(f"Não foram encontradas ideias de saas para o post {post.id} no idioma ingles")
            if gemini_analysis.get("pt"):
                self._save_saas_ideas(post.id, gemini_analysis.get("pt").get("post_analysis"), "pt")
            else:
                logger.warning(f"Não foram encontradas ideias de saas para o post {post.id} no idioma portugues")
        else:
            logger.warning(f"Não foram encontradas ideias de saas para o post {post.id}")

        self.database_gateway.update_post_analysis(post.id)
        logger.info(f"Post {post.id} analyzed")

    def _save_saas_ideas(self, post_id: str, gemini_analysis: dict, lang: str) -> None:
        """Adds a saas idea to the database."""
        try:
            if gemini_analysis and gemini_analysis.get(
                    "insights"):
                logger.info(f"Salvando ideias de SaaS para post {post_id} no idioma {lang}")
                if lang == "en":
                    self._save_saas_ideas_en(post_id, gemini_analysis)
                elif lang == "pt":
                    self._save_saas_ideas_pt(post_id, gemini_analysis)
            else:
                logger.info(f"Não foram encontradas ideias de SaaS para o post {post_id} no idioma {lang}")
        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar ideia saas para o post com ID {post_id}: {e}")

    def _save_saas_ideas_en(self, post_id: str, gemini_analysis_en: dict) -> None:
        """Adds a saas idea to the database in English."""
        for idea_data_en in gemini_analysis_en["insights"]:
            if idea_data_en and idea_data_en.get("saas_product"):
                saas_product_en = idea_data_en.get("saas_product")
                saas_idea_db = SaasIdeaDB(
                    name=saas_product_en.get("name"),
                    description=saas_product_en.get("description"),
                    differentiators=saas_product_en.get("differentiators"),
                    features=saas_product_en.get("features"),
                    implementation_score=saas_product_en.get("implementation_score"),
                    market_viability_score=saas_product_en.get("market_viability_score"),
                    category=saas_product_en.get("category"),
                    post_id=post_id
                )
                self.database_gateway.saas_idea_repository.add_saas_idea(saas_idea_db)
                logger.info(f"Ideia de SaaS '{saas_product_en.get('name')}' salva para o post {post_id} no idioma en")

    def _save_saas_ideas_pt(self, post_id: str, gemini_analysis_pt: dict) -> None:
        """Adds a saas idea to the database in Portuguese."""
        for idea_data_pt in gemini_analysis_pt["insights"]:
            if idea_data_pt and idea_data_pt.get("saas_product"):
                saas_product_pt = idea_data_pt.get("saas_product")
                saas_idea_pt_db = SaasIdeaPtDB(
                    name=saas_product_pt.get("name"),
                    description=saas_product_pt.get("description"),
                    differentiators=saas_product_pt.get("differentiators"),
                    features=saas_product_pt.get("features"),
                    implementation_score=saas_product_pt.get("implementation_score"),
                    market_viability_score=saas_product_pt.get("market_viability_score"),
                    category=saas_product_pt.get("category"),
                    post_id=post_id
                )
                self.database_gateway.saas_idea_pt_repository.add_saas_idea_pt(saas_idea_pt_db)
                logger.info(f"Ideia de SaaS '{saas_product_pt.get('name')}' salva para o post {post_id} no idioma pt")
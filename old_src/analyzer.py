from old_src.core import GeminiAPI
from old_src.database.posts_db import PostsDB
from old_src.database import IdeasDB
from old_src.database.analyzed_posts_db import AnalyzedPostsDB
from old_src.utils.logger import logger
from old_src.config.config import Config
from old_src.models import Idea
import time
import traceback


def main():
    Config()
    gemini_api = GeminiAPI()
    posts_db = PostsDB()
    ideas_db = IdeasDB()
    analyzed_posts_db = AnalyzedPostsDB()
    if not gemini_api.model:
        logger.error("Não foi possível iniciar a aplicação pois não foi estabelecida a conexão com a API do Gemini")
        return
    try:
      while True:
            # Busca o proximo post para analisar
            post = posts_db.get_next_reddit_post()
            if not post:
                logger.info("Não há posts para analisar, aguardando...")
                time.sleep(60)  # Espera por 1 minuto antes de verificar novamente
                continue

            post_id = post[2]
            subreddit_id = post[1]
            combined_text = post[3]

            if analyzed_posts_db.is_duplicate_post(post_id):
                logger.info(f"Post {post_id} já foi analisado")
                posts_db.delete_reddit_post(post_id)
                continue

            logger.info(f"Iniciando análise do post: {post_id}")

            # Analisa o texto usando a API do Gemini
            analysis_result = gemini_api.analyze_with_gemini(combined_text)
            if analysis_result and analysis_result.get("post_analysis").get("insights"):
                analysis_result_list = analysis_result.get("post_analysis").get("insights")
                for result in analysis_result_list:
                    idea = Idea(
                        reddit_content_id=post_id,
                        product_name=result.get("saas_product").get('name'),
                        problem=result.get('problem'),
                        solution_description=result.get("saas_product").get('description'),
                        implementation_score=result.get("saas_product").get('implementation_score'),
                        market_viability_score=result.get("saas_product").get('market_viability_score'),
                        differentials=result.get("saas_product").get('differentiators'),
                        features=result.get("saas_product").get('features'),
                    )
                    if ideas_db.add_idea(idea):
                        logger.info(f"Ideia adicionada: {idea}")
                    else:
                        logger.warning(f"Não foi possível adicionar a ideia, pois ela já existe na base")
                if posts_db.delete_reddit_post(post_id):
                    logger.info(f"Post com id {post_id} deletado com sucesso!")
                    analyzed_posts_db.add_analyzed_post(post_id)
                else:
                     logger.warning(f"Não foi possível deletar o post com id {post_id}")
            else:
                logger.warning(f"Não foi encontrada uma ideia para o post: {post_id}")
            #Adiciona um delay entre as chamadas para não sobrecarregar
            time.sleep(5)
    except Exception as e:
            logger.error(f"Erro inesperado durante a analise: {e}")
            logger.error(traceback.format_exc())
            time.sleep(60)
    finally:
        ideas_db.close_connection()
        posts_db.close_connection()
        analyzed_posts_db.close_connection()

if __name__ == "__main__":
    main()
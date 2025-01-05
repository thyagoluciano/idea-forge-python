from old_src.core import RedditAPI
from old_src.core import GeminiAPI
from old_src.models import Idea
from old_src.database import PostgresDatabase
from old_src.utils.logger import logger
from old_src.config.config import Config


def main():
    Config()
    reddit_api = RedditAPI()
    gemini_api = GeminiAPI()
    idea_db = PostgresDatabase()

    if not reddit_api.reddit:
        logger.error("Não foi possível iniciar a aplicação pois não foi estabelecida a conexão com a API do Reddit")
        return

    if not gemini_api.model:
        logger.error("Não foi possível iniciar a aplicação pois não foi estabelecida a conexão com a API do Gemini")
        return

    # Obtém posts e comentários do Reddit
    posts_data = reddit_api.get_posts_and_comments()

    for post in posts_data:
        full_text = f"Post: {post['title']}\n{post['text']}\n"
        logger.info(f"Analisando o post: {post['title']} ({post['id']})")
        logger.info(f"Upvotes: {post['upvotes']}, Número de comentários: {post['num_comments']}")
        for comment in post['comments']:
            full_text += f"Comment: {comment['text']}\n"
            logger.info(f"  - {comment['author']}: {comment['text'][:50]}... (Upvotes: {comment['upvotes']})")

        # Analisa o texto usando a API do Gemini
        analysis_result = gemini_api.analyze_with_gemini(full_text)

        if analysis_result and analysis_result.get("post_analysis").get("insights"):
            analysis_result_list = analysis_result.get("post_analysis").get("insights")
            for result in analysis_result_list:
                idea = Idea(
                    reddit_content_id=post['id'],
                    product_name=result.get("saas_product").get('name'),
                    problem=result.get('problem'),
                    solution_description=result.get("saas_product").get('description'),
                    implementation_score=result.get("saas_product").get('implementation_score'),
                    market_viability_score=result.get("saas_product").get('market_viability_score'),
                    differentials=result.get("saas_product").get('differentiators'),
                    features=result.get("saas_product").get('features'),
                )
                if idea_db.add_idea(idea):
                    logger.info(f"Ideia adicionada: {idea}")
                    print(f"Ideia adicionada com sucesso: {idea.product_name}")
                else:
                    logger.warning(f"Não foi possível adicionar a ideia, pois ela já existe na base")
                    print(f"Ideia com ID {idea.reddit_content_id} já existe.")
        else:
            logger.warning(f"Não foi encontrada uma ideia para o post: {post['title']}")
        # Adiciona o ID do post aos posts analisados
        if not idea_db.add_analyzed_post(post['id']):
            logger.warning(f"Não foi possível adicionar o post {post['id']} aos posts analisados")

    print("\nExtração e análise concluída!")

    for idea in idea_db.get_all_ideas():
        print(f"Ideia: {idea}")
    idea_db.close_connection()


if __name__ == "__main__":
    main()
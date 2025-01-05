from core.reddit_api import RedditAPI
from database.subreddits_db import SubredditsDB
from database.posts_db import PostsDB
from utils.logger import logger
from config.config import Config
import time
import datetime
import traceback


def main():
    Config()
    reddit_api = RedditAPI()
    subreddits_db = SubredditsDB()
    posts_db = PostsDB()

    if not reddit_api.reddit:
        logger.error("Não foi possível iniciar a aplicação pois não foi estabelecida a conexão com a API do Reddit")
        return

    while True:
        try:
          # Busca o proximo subreddit agendado para extrair posts
          subreddit_to_extract = subreddits_db.get_subreddits_to_extract()

          if not subreddit_to_extract:
              logger.info("Não há subreddits para extrair dados, aguardando...")
              time.sleep(60)  # Espera por 1 minuto antes de verificar novamente
              continue

          subreddit_data = subreddit_to_extract[0]
          subreddit_id = subreddit_data[0]
          subreddit_name = subreddit_data[1]
          sort_type = subreddit_data[2]
          limit_posts = subreddit_data[3]
          last_extraction_date = subreddit_data[4]

          logger.info(f"Iniciando a extração do subreddit: {subreddit_name}")

          # Extrai os posts do subreddit
          posts_data = reddit_api.get_posts_and_comments(subreddit_name, limit_posts, sort_type, last_extraction_date)

          for post in posts_data:
              # Combina o título, conteúdo e comentários em um único texto
              combined_text = f"Post: {post['title']}\n{post['text']}\n"
              for comment in post['comments']:
                  combined_text += f"Comment: {comment['text']}\n"

              # Adiciona o post e seus comentarios na tabela reddit_content
              if posts_db.add_reddit_post(subreddit_id, post['id'], combined_text):
                  logger.info(f"Post '{post['title']}' do subreddit '{subreddit_name}' adicionado com sucesso.")
              else:
                  logger.warning(f"Não foi possível adicionar o post '{post['title']}' do subreddit '{subreddit_name}'")

          # Atualiza a data da ultima extração do subreddit
          subreddits_db.update_subreddit_extraction_date(subreddit_id)
          logger.info(f"Extração do subreddit '{subreddit_name}' finalizada.")

           # Adiciona um delay antes de processar o proximo subreddit
          time.sleep(5)

        except Exception as e:
            logger.error(f"Erro inesperado durante a extração: {e}")
            logger.error(traceback.format_exc())
            time.sleep(60)


if __name__ == "__main__":
    main()
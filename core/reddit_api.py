import praw
import time
from datetime import datetime, timedelta
from config.config import Config
from utils.helpers import clean_text
from utils.logger import logger

class RedditAPI:
    def __init__(self):
        self.config = Config()
        try:
            self.reddit = praw.Reddit(
                client_id=self.config.REDDIT_CLIENT_ID,
                client_secret=self.config.REDDIT_CLIENT_SECRET,
                user_agent=self.config.REDDIT_USER_AGENT
            )
            logger.info("Conexão com Reddit estabelecida com sucesso.")
        except praw.exceptions.PRAWException as e:
            logger.error(f"Erro ao conectar com o Reddit: {e}")
            self.reddit = None

    def get_posts_and_comments(self, subreddit_name, limit, sort_by, last_extraction_date=None, after = None):
        """
            Obtém posts e seus comentários de um subreddit, utilizando paginação e respeitando os limites da API.

            Args:
                subreddit_name: Nome do subreddit a ser pesquisado.
                limit: Número máximo de posts a serem recuperados por requisição.
                sort_by: Tipo de ordenação ('hot', 'top', 'new', 'controversial').
                last_extraction_date: Data e hora da ultima extração para busca paginada.
                after: Id do post para paginação

            Returns:
                Uma lista de dicionários, onde cada dicionário representa um post e seus comentários.
        """
        posts_data = []
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            if sort_by == 'hot':
                posts = subreddit.hot(limit=limit, params={'after': after})
            elif sort_by == 'top':
                posts = subreddit.top(limit=limit, params={'after': after})
            elif sort_by == 'new':
                posts = subreddit.new(limit=limit, params={'after': after})
            elif sort_by == 'controversial':
                posts = subreddit.controversial(limit=limit, params={'after': after})
            else:
                raise ValueError("Invalid sort_by option")

            if last_extraction_date:
                last_extraction_date = datetime.fromisoformat(str(last_extraction_date).replace('Z', '+00:00'))
            else:
                last_extraction_date = datetime.now() - timedelta(weeks=1)

            logger.info(f"Iniciando busca paginada do subreddit '{subreddit_name}'. Last extraction date: {last_extraction_date}, Before: {after}")

            all_posts = []
            last_post_created_date = None
            while True:
              new_posts = 0
              for post in posts:
                post_created_date = datetime.fromtimestamp(post.created_utc)
                if  not last_post_created_date or post_created_date < last_extraction_date:
                     last_post_created_date = post_created_date
                post_data = {
                    "title": post.title,
                    "id": post.id,
                    "url": post.url,
                    "text": clean_text(post.selftext) if hasattr(post, 'selftext') else "",
                    "num_comments": post.num_comments,
                    "upvotes": post.ups,
                    "comments": []
                }
                post.comments.replace_more(limit=0)
                for comment in post.comments.list():
                   post_data["comments"].append({
                        "author": comment.author.name if comment.author else "[deleted]",
                        "text": clean_text(comment.body),
                        "created": str(datetime.fromtimestamp(comment.created_utc)),
                        "upvotes": comment.ups
                    })
                all_posts.append(post_data)
                new_posts+=1
                time.sleep(1)
              if new_posts == 0 or last_post_created_date < last_extraction_date:
                logger.info(f"Busca paginada do subreddit {subreddit_name} finalizada")
                break
              if posts:
                after = posts[-1].fullname
              else:
                after = None
              if sort_by == 'hot':
                  posts = subreddit.hot(limit=limit, params={'after': after})
              elif sort_by == 'top':
                  posts = subreddit.top(limit=limit, params={'after': after})
              elif sort_by == 'new':
                  posts = subreddit.new(limit=limit, params={'after': after})
              elif sort_by == 'controversial':
                  posts = subreddit.controversial(limit=limit, params={'after': after})
            return all_posts
        except praw.exceptions.PRAWException as e:
            logger.error(f"Erro ao obter posts do subreddit {subreddit_name}: {e}")
            return []
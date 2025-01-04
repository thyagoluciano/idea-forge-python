import praw
import time
from datetime import datetime
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

    def get_posts_and_comments(self, subreddit_name=None, limit=None, sort_by=None):
         """
         Obtém posts e seus comentários de um subreddit.

         Args:
             subreddit_name: Nome do subreddit a ser pesquisado.
             limit: Número máximo de posts a serem recuperados.
             sort_by: Tipo de ordenação ('hot', 'top', 'new', 'controversial').

         Returns:
             Uma lista de dicionários, onde cada dicionário representa um post e seus comentários.
         """
         if not subreddit_name:
            subreddit_name = self.config.SUBREDDIT_NAME
         if not limit:
           limit = int(self.config.LIMIT_POSTS)
         if not sort_by:
           sort_by = self.config.SORT_TYPE

         posts_data = []
         try:
             subreddit = self.reddit.subreddit(subreddit_name)

             if sort_by == 'hot':
                 posts = subreddit.hot(limit=limit)
             elif sort_by == 'top':
                 posts = subreddit.top(limit=limit)
             elif sort_by == 'new':
                 posts = subreddit.new(limit=limit)
             elif sort_by == 'controversial':
                 posts = subreddit.controversial(limit=limit)
             else:
                 raise ValueError("Invalid sort_by option")

             for post in posts:
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
                 posts_data.append(post_data)
                 time.sleep(1)
         except praw.exceptions.PRAWException as e:
             logger.error(f"Erro ao obter posts do subreddit {subreddit_name}: {e}")
         return posts_data
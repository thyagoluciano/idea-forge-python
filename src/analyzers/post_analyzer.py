from src.core.gemini_api import GeminiAPI
from src.database.database_manager import DatabaseManager
from src.models.database_models import PostDB


class PostAnalyzer:
    def __init__(self):
        self.gemini_api = GeminiAPI()
        self.database_manager = DatabaseManager()

    def analyze_posts(self):
        session = self.database_manager.Session()
        try:
            posts = session.query(PostDB).filter(PostDB.gemini_analysis.is_(None)).all()
            for post in posts:
                text_to_analyze = f"{post.title} \n {post.text} \n {' '.join([comment.text for comment in post.comments])}"
                gemini_analysis = self.gemini_api.analyze_with_gemini(text_to_analyze, post.title)
                self.database_manager.add_post(post, gemini_analysis)
                print(f"Post {post.id} analyzed")

        except Exception as e:
            print(f"Erro ao analisar os posts: {e}")
        finally:
            session.close()

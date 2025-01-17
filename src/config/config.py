# src/config/config.py
import os
from dotenv import load_dotenv
import json

load_dotenv()


class Config:
    # Reddit API
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

    # Gemini API
    GOOGLE_API_KEYS = os.getenv("GOOGLE_API_KEYS")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", 'gemini-pro')  # Default gemini-pro

    # Project Settings
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME", "Entrepreneur")
    LIMIT_POSTS = os.getenv("LIMIT_POSTS", 10)
    SORT_TYPE = os.getenv("SORT_TYPE", 'hot')

    # PostgreSQL Database
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "idea_forge")

    def __init__(self):
        self.google_api_keys = self._load_api_keys()
        self._validate_required_vars()

    @staticmethod
    def _load_api_keys():
        """Loads and validates API keys from environment variable."""
        keys_str = os.getenv("GOOGLE_API_KEYS", '[]')
        try:
            keys = json.loads(keys_str)
            if not isinstance(keys, list) or not all(isinstance(key, str) for key in keys):
                raise ValueError("GOOGLE_API_KEYS must be a JSON list of strings.")
            return keys
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format for GOOGLE_API_KEYS.")
        except ValueError as e:
            raise e

    def _validate_required_vars(self):
        """Validate required environment variables."""
        required_vars = {
            "REDDIT_CLIENT_ID": self.REDDIT_CLIENT_ID,
            "REDDIT_CLIENT_SECRET": self.REDDIT_CLIENT_SECRET,
            "REDDIT_USER_AGENT": self.REDDIT_USER_AGENT,
            "POSTGRES_USER": self.POSTGRES_USER,
            "POSTGRES_PASSWORD": self.POSTGRES_PASSWORD,
        }

        for var, value in required_vars.items():
            if not value:
                raise ValueError(f"Missing required environment variable: {var}")
        if not self.google_api_keys:
            raise ValueError(f"Missing required environment variable: GOOGLE_API_KEYS")
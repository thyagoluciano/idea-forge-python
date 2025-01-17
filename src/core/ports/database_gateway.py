# src/core/ports/database_gateway.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.entities import Post


class DatabaseGateway(ABC):
    @abstractmethod
    def add_post(self, post: Post) -> Optional[str]:
        pass

    @abstractmethod
    def add_saas_ideas(self, post_id: str, gemini_analysis: dict) -> None:
        pass

    @property
    @abstractmethod
    def saas_idea_repository(self):
        pass

    @property
    @abstractmethod
    def saas_idea_pt_repository(self):
        pass

    @abstractmethod
    def post_exists(self, post_id: str) -> bool:
        pass

    @abstractmethod
    def post_already_analyzed(self, post_id: str) -> bool:
        pass

    @abstractmethod
    def add_extraction_config(self, config_data: dict) -> None:
        pass

    @abstractmethod
    def get_all_extraction_configs(self) -> List[dict]:
        pass

    @abstractmethod
    def update_extraction_config(self, config_id: int) -> None:
        pass

    @abstractmethod
    def update_post_analysis(self, post_id: str) -> None:
        pass

    @abstractmethod
    def get_posts_to_analyze(self, batch_size: int = 10) -> List[Post]:
        pass
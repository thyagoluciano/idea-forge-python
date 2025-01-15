# src/core/ports/saas_ideas_gateway.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from src.adapters.models import PaginatedResponse


class SaasIdeasGateway(ABC):
    @abstractmethod
    def list_saas_ideas(
            self,
            implementation_score: Optional[int] = None,
            market_viability_score: Optional[int] = None,
            category: Optional[str] = None,
            features: Optional[str] = None,
            differentiators: Optional[str] = None,
            description: Optional[str] = None,
            page: int = 1,
            page_size: int = 10,
            order_by: Optional[str] = None,
            order_direction: Optional[str] = "asc"
    ) -> PaginatedResponse:
        pass

    @abstractmethod
    def list_all_categories(self) -> List[str]:
        pass
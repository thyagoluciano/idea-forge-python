# src/adapters/models/paginated_response.py
from typing import List
from pydantic import BaseModel

from src.adapters.models.saas_idea import SaasIdea


class PaginatedResponse(BaseModel):
    items: List[SaasIdea]
    total: int
    page: int
    page_size: int

from typing import List, Optional
from pydantic import BaseModel


class SaasIdea(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    differentiators: Optional[List[str]] = None
    features: Optional[List[str]] = None
    implementation_score: Optional[int] = None
    market_viability_score: Optional[int] = None
    category: Optional[str] = None
    post_id: str

    class Config:
        from_attributes = True

# src/adapters/api/main.py
from typing import List, Optional, Dict
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from src.config.config import Config
from src.core.ports.saas_ideas_gateway import SaasIdeasGateway
from src.adapters.saas_ideas_adapter import SaasIdeasAdapter
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)

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

class PaginatedResponse(BaseModel):
    items: List[SaasIdea]
    total: int
    page: int
    page_size: int

app = FastAPI()

origins = [
    "http://localhost:3000", #  Seu frontend
    "https://ideaforge.bemysaas.com.br"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_saas_ideas_adapter():
    adapter = SaasIdeasAdapter()
    return adapter


@app.get("/saas_ideas", response_model=PaginatedResponse)
def list_saas_ideas(
    category: Optional[str] = Query(None),
    features: Optional[str] = Query(None),
    differentiators: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0),
    order_by: Optional[str] = Query(None, enum=["implementation_score", "market_viability_score", "category"]),
    order_direction: Optional[str] = Query("asc", enum=["asc", "desc"]),
    saas_ideas_gateway: SaasIdeasGateway = Depends(get_saas_ideas_adapter)
):
    try:
        saas_ideas = saas_ideas_gateway.list_saas_ideas(
            category=category,
            features=features,
            differentiators=differentiators,
            description=description,
            page=page,
            page_size=page_size,
            order_by=order_by,
            order_direction=order_direction
        )
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar ideias Saas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar ideias Saas no banco de dados")

    if not saas_ideas["items"]:
        raise HTTPException(status_code=404, detail="Nenhuma ideia SaaS encontrada com os filtros fornecidos.")

    return saas_ideas

@app.get("/saas_categories", response_model=List[str])
def list_saas_categories(
    saas_ideas_gateway: SaasIdeasGateway = Depends(get_saas_ideas_adapter)
):
    try:
        categories = saas_ideas_gateway.list_all_categories()
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar categorias Saas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar categorias Saas no banco de dados")

    if not categories:
        raise HTTPException(status_code=404, detail="Nenhuma categoria SaaS encontrada.")

    return categories
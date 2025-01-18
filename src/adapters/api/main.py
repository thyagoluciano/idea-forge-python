# src/adapters/api/main.py
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from src.adapters.database_adapter import DatabaseAdapter
from src.adapters.models import PaginatedResponse
from src.core.ports.saas_ideas_gateway import SaasIdeasGateway
from src.adapters.saas_ideas_adapter import SaasIdeasAdapter
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://ideaforge.bemysaas.com.br"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_database_adapter():
    """Dependency to get the database adapter"""
    adapter = DatabaseAdapter()
    return adapter


def get_saas_ideas_adapter(
    database_adapter: DatabaseAdapter = Depends(get_database_adapter),
    accept_language: str = Header(default="en-US")
):
    """Dependency to get the saas ideas adapter based on language"""
    table_name = "saas_ideas_pt" if accept_language.startswith("pt") else "saas_ideas"
    adapter = SaasIdeasAdapter(table_name=table_name)
    return adapter


@app.get("/saas_ideas", response_model=PaginatedResponse)
def list_saas_ideas(
        category: Optional[List[str]] = Query(None),
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

    if not saas_ideas.items:
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

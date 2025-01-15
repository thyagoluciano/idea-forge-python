# src/adapters/saas_ideas_adapter.py
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.exc import SQLAlchemyError
from src.config.config import Config
from src.core.ports.saas_ideas_gateway import SaasIdeasGateway
from src.core.utils.logger import setup_logger
from src.adapters.models import SaasIdea, PaginatedResponse
from src.database.models import SaasIdeaDB, PostDB, CommentDB
from sqlalchemy.sql import select, func

logger = setup_logger(__name__)


class SaasIdeasAdapter(SaasIdeasGateway):
    def __init__(self) -> None:
        self.config: Config = Config()
        url: str = f"postgresql://{self.config.POSTGRES_USER}:{self.config.POSTGRES_PASSWORD}@{self.config.POSTGRES_HOST}:{self.config.POSTGRES_PORT}/{self.config.POSTGRES_DB}"
        self.engine = create_engine(url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @staticmethod
    def _build_saas_ideas_query(
            db: sessionmaker,
            category: Optional[str] = None,
            features: Optional[str] = None,
            differentiators: Optional[str] = None,
            description: Optional[str] = None
    ) -> Query:
        with db() as session:  # create the session
            query: Query = session.query(SaasIdeaDB)  # use the session to create the query

            if category is not None:
                query = query.filter(SaasIdeaDB.category == category)
            if features:
                query = query.filter(SaasIdeaDB.features.like(f"%{features}%"))
            if differentiators:
                query = query.filter(SaasIdeaDB.differentiators.like(f"%{differentiators}%"))
            if description:
                query = query.filter(SaasIdeaDB.description.like(f"%{description}%"))

            return query

    def _apply_order_by(self, query: Query, order_by: Optional[str] = None,
                        order_direction: Optional[str] = "asc") -> Query:
        if order_by:
            order_by_column = getattr(SaasIdeaDB, order_by)
            if order_direction == "asc":
                query = query.order_by(asc(order_by_column))
            else:
                query = query.order_by(desc(order_by_column))
        return query

    @staticmethod
    def _paginate_query(query: Query, page: int, page_size: int) -> tuple[List[Any], int]:
        total: int = query.count()
        items: List[Any] = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def _execute_saas_ideas_query(
            self, db: sessionmaker,
            category: Optional[str] = None,
            features: Optional[str] = None,
            differentiators: Optional[str] = None,
            description: Optional[str] = None,
            page: int = 1, page_size: int = 10,
            order_by: Optional[str] = None,
            order_direction: Optional[str] = "asc"
    ) -> Dict:
        try:
            with db() as session:
                query: Query = self._build_saas_ideas_query(session, category, features, differentiators, description)
                query = self._apply_order_by(query, order_by, order_direction)
                items, total = self._paginate_query(query, page, page_size)
                return {
                    "items": [SaasIdea.model_validate(item) for item in items],
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                }
        except SQLAlchemyError as e:
            logger.error(f"Erro ao executar query de ideias saas: {e}")
            return {"items": [], "total": 0, "page": page, "page_size": page_size}
        except Exception as e:
            logger.error(f"Erro inesperado ao executar query de ideias saas: {e}")
            return {"items": [], "total": 0, "page": page, "page_size": page_size}

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
        try:
            response = self._execute_saas_ideas_query(
                self.SessionLocal,
                category,
                features,
                differentiators,
                description,
                page,
                page_size,
                order_by,
                order_direction
            )
            return PaginatedResponse(**response)
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar ideias Saas: {e}")
            return PaginatedResponse(items=[], total=0, page=page, page_size=page_size)
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar ideias Saas: {e}")
            return PaginatedResponse(items=[], total=0, page=page, page_size=page_size)

    def list_all_categories(self) -> List[str]:
        db = self.SessionLocal()
        try:
            categories = db.query(SaasIdeaDB.category).distinct()
            return [category.scalar() for category in categories]
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar categorias: {e}")
            return []
        finally:
            db.close()

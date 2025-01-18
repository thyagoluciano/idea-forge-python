# src/adapters/saas_ideas_adapter.py
import json
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.exc import SQLAlchemyError
from src.config.config import Config
from src.core.ports.saas_ideas_gateway import SaasIdeasGateway
from src.core.utils.logger import setup_logger
from src.adapters.models import SaasIdea, PaginatedResponse
from src.database.models.saas_idea_db import SaasIdeaDB
from src.database.models.saas_idea_pt_db import SaasIdeaPtDB

logger = setup_logger(__name__)


class SaasIdeasAdapter(SaasIdeasGateway):
    def __init__(self, table_name: str = 'saas_ideas') -> None:
        self.config: Config = Config()
        url: str = f"postgresql://{self.config.POSTGRES_USER}:{self.config.POSTGRES_PASSWORD}@{self.config.POSTGRES_HOST}:{self.config.POSTGRES_PORT}/{self.config.POSTGRES_DB}"
        self.engine = create_engine(url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.table_name = table_name
        self.table_class = SaasIdeaDB if table_name == 'saas_ideas' else SaasIdeaPtDB

    def _build_saas_ideas_query(self, db: sessionmaker, category: Optional[str] = None, features: Optional[str] = None,
                                differentiators: Optional[str] = None, description: Optional[str] = None) -> Query:
        with db() as session:
            query: Query = session.query(self.table_class)

            if category is not None:
                query = query.filter(self.table_class.category == category)
            if features:
                query = query.filter(self.table_class.features.like(f"%{features}%"))
            if differentiators:
                query = query.filter(self.table_class.differentiators.like(f"%{differentiators}%"))
            if description:
                query = query.filter(self.table_class.description.like(f"%{description}%"))

            return query

    @staticmethod
    def _apply_order_by(query: Query, order_by: Optional[str] = None,
                        order_direction: Optional[str] = "asc") -> Query:
        if order_by:
            order_by_column = getattr(SaasIdeasAdapter.table_class, order_by)
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

    @staticmethod
    def _deserialize_saas_idea(item: SaasIdeaDB) -> SaasIdea:
        differentiators = None
        features = None

        differentiators_list = []
        features_list = []
        if item.differentiators:
            cleaned_string = item.differentiators.strip('{}')
            differentiators_list = [d.strip('"') for d in cleaned_string.split(',')]
        if item.features:
            cleaned_string = item.features.strip('{}')
            features_list = [f.strip('"') for f in cleaned_string.split(',')]

        return SaasIdea(
            id=item.id,
            name=item.name,
            description=item.description,
            differentiators= differentiators_list,
            features=features_list,
            implementation_score=item.implementation_score,
            market_viability_score=item.market_viability_score,
            category=item.category,
            post_id=item.post_id
        )

    def _execute_saas_ideas_query(self, db: sessionmaker, category: Optional[str] = None,
                                  features: Optional[str] = None,
                                  differentiators: Optional[str] = None, description: Optional[str] = None,
                                  page: int = 1, page_size: int = 10, order_by: Optional[str] = None,
                                  order_direction: Optional[str] = "asc") -> Dict:
        try:
            with db() as session:
                query: Query = self._build_saas_ideas_query(db, category, features, differentiators, description)
                query = self._apply_order_by(query, order_by, order_direction)
                items, total = self._paginate_query(query, page, page_size)
                return {
                    "items": [self._deserialize_saas_idea(item) for item in items],
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
            response = self._execute_saas_ideas_query(self.SessionLocal, category, features, differentiators,
                                                      description, page,
                                                      page_size, order_by, order_direction)
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
            categories = db.query(self.table_class.category).distinct()
            return [category[0] for category in categories]
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar categorias: {e}")
            return []
        finally:
            db.close()
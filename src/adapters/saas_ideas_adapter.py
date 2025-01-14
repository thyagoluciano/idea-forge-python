# src/adapters/saas_ideas_adapter.py
from typing import List, Optional, Dict
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, text, DateTime, Boolean, asc, desc
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError
from src.config.config import Config
from src.core.ports.saas_ideas_gateway import SaasIdeasGateway
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


class SaasIdeasAdapter(SaasIdeasGateway):
    def __init__(self):
        self.config = Config()
        url = f"postgresql://{self.config.POSTGRES_USER}:{self.config.POSTGRES_PASSWORD}@{self.config.POSTGRES_HOST}:{self.config.POSTGRES_PORT}/{self.config.POSTGRES_DB}"
        self.engine = create_engine(url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base = declarative_base()

        class SaasIdeaDB(Base):
            __tablename__ = "saas_ideas"

            id = Column(Integer, primary_key=True, autoincrement=True)
            name = Column(String, nullable=False)
            description = Column(String)
            differentiators = Column(JSON)
            features = Column(JSON)
            implementation_score = Column(Integer)
            market_viability_score = Column(Integer)
            category = Column(String)
            post_id = Column(String, ForeignKey("posts.id"))
            post = relationship("PostDB")

        class PostDB(Base):
            __tablename__ = "posts"

            id = Column(String, primary_key=True)
            title = Column(String, nullable=False)
            url = Column(String, nullable=False)
            text = Column(String)
            num_comments = Column(Integer)
            ups = Column(Integer)
            created_at = Column(DateTime)
            gemini_analysis = Column(Boolean, default=False)
            comments = relationship("CommentDB", back_populates="post", cascade="all, delete-orphan")

        class CommentDB(Base):
            __tablename__ = "comments"

            id = Column(Integer, primary_key=True, autoincrement=True)
            author = Column(String)
            text = Column(String)
            created_utc = Column(DateTime)
            ups = Column(Integer)
            post_id = Column(String, ForeignKey("posts.id"))
            post = relationship("PostDB", back_populates="comments")

        self.SaasIdeaDB = SaasIdeaDB
        self.PostDB = PostDB
        self.CommentDB = CommentDB

    def list_saas_ideas(
            self,
            category: Optional[str] = None,
            features: Optional[str] = None,
            differentiators: Optional[str] = None,
            description: Optional[str] = None,
            page: int = 1,
            page_size: int = 10,
            order_by: Optional[str] = None,
            order_direction: Optional[str] = "asc"
    ) -> Dict:
        db = self.SessionLocal()
        try:
            query = db.query(self.SaasIdeaDB)

            if category is not None:
                query = query.filter(self.SaasIdeaDB.category == category)

            if features:
                query = query.filter(self.SaasIdeaDB.features.like(f"%{features}%"))
            if differentiators:
                query = query.filter(self.SaasIdeaDB.differentiators.like(f"%{differentiators}%"))
            if description:
                query = query.filter(self.SaasIdeaDB.description.like(f"%{description}%"))

            if order_by:
                order_by_column = getattr(self.SaasIdeaDB, order_by)
                if order_direction == "asc":
                    query = query.order_by(asc(order_by_column))
                else:
                    query = query.order_by(desc(order_by_column))

            total = query.count()
            saas_ideas = query.offset((page - 1) * page_size).limit(page_size).all()
            return {
                "items": [idea.__dict__ for idea in saas_ideas],
                "total": total,
                "page": page,
                "page_size": page_size,
            }
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar ideias Saas: {e}")
            return {"items": [], "total": 0, "page": page, "page_size": page_size}

        finally:
            db.close()

    def list_all_categories(self) -> List[str]:
        db = self.SessionLocal()
        try:
            categories = db.query(self.SaasIdeaDB.category).distinct().all()
            return [category[0] for category in categories if category[0]]
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar categorias: {e}")
            return []
        finally:
            db.close()
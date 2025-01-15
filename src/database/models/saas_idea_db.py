# src/database/models/saas_idea_db.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.database.models.database_models import Base
from src.database.models.post_db import PostDB


class SaasIdeaDB(Base):
    __tablename__ = "saas_ideas"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    differentiators = Column(JSON)
    features = Column(JSON)
    implementation_score = Column(Integer)
    market_viability_score = Column(Integer)
    category = Column(String)
    post_id = Column(String, ForeignKey("posts.id"))
    post = relationship(PostDB)
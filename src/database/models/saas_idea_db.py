# src/database/models/saas_idea_db.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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
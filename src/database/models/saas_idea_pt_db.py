from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Boolean, Text
from sqlalchemy.orm import relationship

from src.database.models.category_db import CategoryDB
from src.database.models.database_models import Base
from src.database.models.post_db import PostDB


class SaasIdeaPtDB(Base):
    __tablename__ = "saas_ideas_pt"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    differentiators = Column(Text)
    features = Column(Text)
    implementation_score = Column(Integer)
    market_viability_score = Column(Integer)
    post_id = Column(String, ForeignKey("posts.id"))
    post = relationship(PostDB)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship(CategoryDB)

# src/database/models/post_db.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from src.database.models.database_models import Base


class PostDB(Base):
    __tablename__ = "posts"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    text = Column(String)
    num_comments = Column(Integer)
    ups = Column(Integer)
    created_at = Column(DateTime)
    gemini_analysis = Column(Boolean, default=False)
    comments = relationship("CommentDB", back_populates="post", cascade="all, delete-orphan")
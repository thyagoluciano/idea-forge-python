# src/database/models/post_db.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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

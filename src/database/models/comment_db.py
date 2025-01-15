# src/database/models/comment_db.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CommentDB(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String)
    text = Column(String)
    created_utc = Column(DateTime)
    ups = Column(Integer)
    post_id = Column(String, ForeignKey("posts.id"))
    post = relationship("PostDB", back_populates="comments")

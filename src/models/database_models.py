from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
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

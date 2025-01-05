from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
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


class ExtractionConfigDB(Base):
    __tablename__ = "extraction_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False) # subreddit or search
    subreddit_name = Column(String)
    query = Column(String)
    sort_criteria = Column(String, nullable=False)
    batch_size = Column(Integer, default=10)
    days_ago = Column(Integer, default=1)
    limit = Column(Integer)
    schedule_time = Column(String) # Store time as HH:MM
    daily = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)
    last_run = Column(DateTime)

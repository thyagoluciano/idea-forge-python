# src/database/models/extraction_config_db.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.database.models.database_models import Base


class ExtractionConfigDB(Base):
    __tablename__ = "extraction_configs"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)  # subreddit or search
    subreddit_name = Column(String)
    query = Column(String)
    sort_criteria = Column(String, nullable=False)
    batch_size = Column(Integer, default=10)
    days_ago = Column(Integer, default=1)
    limit = Column(Integer)
    schedule_time = Column(String)  # Store time as HH:MM
    daily = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)
    last_run = Column(DateTime)
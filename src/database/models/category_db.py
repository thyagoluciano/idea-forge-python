# src/database/models/category_db.py
from sqlalchemy import Column, Integer, String
from src.database.models.database_models import Base


class CategoryDB(Base):
    __tablename__ = "categories"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_en = Column(String, nullable=False)
    category_pt = Column(String, nullable=False)
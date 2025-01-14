# src/core/entities.py
from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Comment:
    """Represents a Reddit comment."""
    author: str
    text: str
    created_utc: datetime
    ups: int


@dataclass
class Post:
    """Represents a Reddit post."""
    title: str
    id: str
    url: str
    text: str
    num_comments: int
    ups: int
    comments: List[Comment]

import datetime
from dataclasses import dataclass


@dataclass
class Comment:
    """Represents a Reddit comment."""
    author: str
    text: str
    created_utc: datetime
    ups: int

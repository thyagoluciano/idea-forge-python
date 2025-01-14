from dataclasses import dataclass
from typing import List

from old.models.comment_models import Comment


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
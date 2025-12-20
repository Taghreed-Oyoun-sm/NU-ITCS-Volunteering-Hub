from pydantic import BaseModel
from typing import Optional, List

class PostCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class CommentCreate(BaseModel):
    content: str
    parent_id: int | None = None


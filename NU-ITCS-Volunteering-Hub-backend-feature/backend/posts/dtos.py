from pydantic import BaseModel
from typing import Optional, List

class PostCreate(BaseModel):
    student_id: int
    title: str
    content: str
    tags: List[str] = []

class CommentCreate(BaseModel):
    student_id: int
    post_id: int
    content: str
    parent_id: Optional[int] = None

from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    student_id: int
    content: str

class CommentCreate(BaseModel):
    student_id: int
    post_id: int
    content: str
    parent_id: Optional[int] = None

from pydantic import BaseModel
from typing import Optional, List

class CommentCreate(BaseModel):
    content: str
    post_id: int
    parent_id: Optional[int] = None

class CommentOut(BaseModel):
    id: int
    content: str
    post_id: int
    parent_id: Optional[int]

    class Config:
        from_attributes = True 
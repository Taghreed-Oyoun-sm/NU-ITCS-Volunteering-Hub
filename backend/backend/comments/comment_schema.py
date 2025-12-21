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
<<<<<<< HEAD
        from_attributes = True
=======
        from_attributes = True 
>>>>>>> 979f903 (Backend and APIS)

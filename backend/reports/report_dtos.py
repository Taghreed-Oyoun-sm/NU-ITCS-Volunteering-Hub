from pydantic import BaseModel
from typing import Optional

class ReportCreate(BaseModel):
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    reason: str

class ReportOut(BaseModel):
    id: int
    reason: str

    class Config:
        from_attributes = True

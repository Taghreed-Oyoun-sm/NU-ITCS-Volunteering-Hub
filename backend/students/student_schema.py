from pydantic import BaseModel, EmailStr
from typing import List, Optional

class StudentCreate(BaseModel):
    student_id: int
    name: str
    email: EmailStr
    year: str
    track: str
    cgpa: float
    # research_skills: bool = False
    # jta_skills: bool = False
    password: str
    strength_areas: List[str] = [] # Received as a list from frontend

class StudentResponse(BaseModel):
    student_id: int
    name: str
    email: EmailStr
    year: str
    track: str
    cgpa: float
    # research_skills: bool
    # jta_skills: bool
    strength_areas: Optional[str] = None # Returned as a string from DB

    class Config:
        from_attributes = True
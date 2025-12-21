from pydantic import BaseModel, EmailStr
from typing import List, Optional

class StudentCreate(BaseModel):
<<<<<<< HEAD
=======
    student_id: int
>>>>>>> 979f903 (Backend and APIS)
    name: str
    email: EmailStr
    year: str
    track: str
    cgpa: float
<<<<<<< HEAD
    research_skills: bool = False
    jta_skills: bool = False
=======
    # research_skills: bool = False
    # jta_skills: bool = False
>>>>>>> 979f903 (Backend and APIS)
    password: str
    strength_areas: List[str] = [] # Received as a list from frontend

class StudentResponse(BaseModel):
<<<<<<< HEAD
    id: int
=======
    student_id: int
>>>>>>> 979f903 (Backend and APIS)
    name: str
    email: EmailStr
    year: str
    track: str
    cgpa: float
<<<<<<< HEAD
    research_skills: bool
    jta_skills: bool
=======
    # research_skills: bool
    # jta_skills: bool
>>>>>>> 979f903 (Backend and APIS)
    strength_areas: Optional[str] = None # Returned as a string from DB

    class Config:
        from_attributes = True
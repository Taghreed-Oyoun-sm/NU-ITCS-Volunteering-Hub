from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List
from enum import Enum

class Track(str, Enum):
    CS = "CS"
    AI = "AI"
    BMD = "BMD"
    CyberSecurity = "CyberSecurity"

class Year(str, Enum):
    Freshman = "Freshman"
    Sophomore = "Sophomore"
    Junior = "Junior"
    Senior = "Senior"

class UserCreate(BaseModel):
    student_id: int
    name: str = Field(..., min_length=2)
    email: EmailStr
    year: Year
    track: Track
    cgpa: float
<<<<<<< HEAD
    research_skills: bool = False
    jta_skills: bool = False
=======
    # research_skills: bool = False
    # jta_skills: bool = False
>>>>>>> 979f903 (Backend and APIS)
    password: str = Field(..., min_length=6, max_length=72)
    strength_areas: List[str] = []

    @field_validator("cgpa")
    def validate_cgpa(cls, v):
        if not (0.0 <= v <= 4.0):
            raise ValueError("CGPA must be between 0.0 and 4.0")
        return v

class UserOut(BaseModel):
    student_id: int
    name: str
    email: EmailStr
    year: Year
    track: Track
    cgpa: float
    # research_skills: bool
    # jta_skills: bool

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

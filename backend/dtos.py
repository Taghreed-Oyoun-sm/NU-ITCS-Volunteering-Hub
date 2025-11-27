from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum

#Fixed values, user can't input any value outside it 
class Role(str, Enum): 
    Student = "Student"
    TA = "TA"
    Dr = "Dr"
    Club = "Club"

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

#schema for signup input
class UserCreate(BaseModel):
    student_id: str
    name: str = Field(..., min_length=2)
    email: EmailStr
    year: Year
    track: Track
    cgpa: float
    role: Role
    #For input validation
    research_skills: bool = False
    jta_skills: bool = False
    password: str = Field(..., min_length=6, max_length=72)

    class Config:
        orm_mode = True

    @field_validator("cgpa")
    def validate_cgpa(cls, v):
        if not (0.0 <= v <= 4.0):
            raise ValueError("CGPA must be between 0.0 and 4.0")
        return v
    
# Schema for output
class UserOut(BaseModel):
    student_id: str
    name: str
    email: EmailStr
    year: Year
    track: Track
    cgpa: float
    research_skills: bool
    jta_skills: bool

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# JWT token schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

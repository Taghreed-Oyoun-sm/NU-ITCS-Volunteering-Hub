from pydantic import BaseModel, EmailStr


class StudentLogin(BaseModel):
    email: EmailStr
    password: str

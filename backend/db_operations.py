from sqlalchemy.orm import Session
from .student_model import Student
from .dtos import UserCreate
from .password_handling import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()

def create_user(db: Session, user_in: UserCreate):
    hashed = hash_password(user_in.password)
    db_user = Student(
        student_id=user_in.student_id,
        name=user_in.name,
        email=user_in.email,
        year=user_in.year.value,          
        track=user_in.track.value,        
        cgpa=user_in.cgpa,
        research_skills=user_in.research_skills,
        jta_skills=user_in.jta_skills,  
        hashed_password=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

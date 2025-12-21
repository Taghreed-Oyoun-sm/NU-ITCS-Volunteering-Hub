from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter, Depends, HTTPException, Query
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import List 
from typing import List, Optional


from backend.db_connection import get_db
from backend.students.student_model import Student
from backend.students.student_schema import StudentCreate, StudentResponse
from backend.students.schemas import StudentLogin
from backend.students.db_operations import get_user_by_email
from backend.students.security import hash_password, verify_password

SECRET_KEY = "secret123"
ALGORITHM = "HS256"
security = HTTPBearer()


router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/signup", response_model=StudentResponse)
def signup(user_in: StudentCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Convert list to string for DB storage
    skills_str = ",".join(user_in.strength_areas) if user_in.strength_areas else ""

    student = Student(
<<<<<<< HEAD
=======
        student_id=user_in.student_id,
>>>>>>> 979f903 (Backend and APIS)
        name=user_in.name,
        email=user_in.email,
        year=user_in.year,
        track=user_in.track,
        cgpa=user_in.cgpa,
<<<<<<< HEAD
        research_skills=user_in.research_skills,
        jta_skills=user_in.jta_skills,
=======
        # research_skills=user_in.research_skills,
        # jta_skills=user_in.jta_skills,
>>>>>>> 979f903 (Backend and APIS)
        strength_areas=skills_str, # Store as string
        hashed_password=hash_password(user_in.password),
    )

    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.post("/login")
def login(user_in: StudentLogin, db: Session = Depends(get_db)):

    student = get_user_by_email(db, user_in.email)

    if not student or not verify_password(user_in.password, student.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

<<<<<<< HEAD
    token = jwt.encode({"sub": str(student.id)}, SECRET_KEY, algorithm=ALGORITHM)
=======
    token = jwt.encode({"sub": str(student.student_id)}, SECRET_KEY, algorithm=ALGORITHM)
>>>>>>> 979f903 (Backend and APIS)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
def get_current_student(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        student_id = student_id = int(payload.get("sub"))

        if student_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

<<<<<<< HEAD
    student = db.query(Student).filter(Student.id == student_id).first()
=======
    student = db.query(Student).filter(Student.student_id == student_id).first()
>>>>>>> 979f903 (Backend and APIS)

    if student is None:
        raise HTTPException(status_code=401, detail="Student not found")

    return student


# PROFILE & MATCHING
# ---------------------------------------------------

@router.get("/me", response_model=StudentResponse)
def get_my_profile(current_student: Student = Depends(get_current_student)):
    """
    Get the profile of the currently logged-in student.
    """
    return current_student

@router.get("/match-by-tags", response_model=List[StudentResponse])
def match_students_by_tags(
    tags: str = Query(..., description="Comma-separated tags to match, e.g., 'Python,AI'"),
    db: Session = Depends(get_db)
):
    """
    Find students who have skills matching the provided tags string.
    """
    # 1. Prepare search tags (lowercase for better matching)
    search_tags = [t.strip().lower() for t in tags.split(",") if t.strip()]
    
    if not search_tags:
        return []

    # 2. Get all students and filter by skill overlap
    all_students = db.query(Student).all()
    matched_students = []

    for student in all_students:
        if student.strength_areas:
            # Convert DB string "Python,Java" -> ["python", "java"]
            student_skills = [s.strip().lower() for s in student.strength_areas.split(",") if s.strip()]
            
            # Check if any search tag exists in the student's skills
            if any(tag in student_skills for tag in search_tags):
                matched_students.append(student)

    return matched_students
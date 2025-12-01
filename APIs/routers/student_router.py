# This file contains all API endpoints related to Students:
# signup, login, profile retrieval, and token-based authentication.

from fastapi import APIRouter, Depends, HTTPException, Header, Body
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.db_operations import get_user_by_email, create_user
from backend.dtos import UserCreate, UserOut, UserLogin, Token
from backend.password_handling import verify_password
from backend.JWT_auth import create_access_token, decode_token
from backend.db_connection import SessionLocal  

router = APIRouter(prefix="/students", tags=["Students"])

# ---------------------------
# DB dependency
# ---------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# OAuth2 scheme to get token from headers
# ---------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/students/login")

# ---------------------------
# SIGNUP
# ---------------------------

@router.post("/signup", response_model=UserOut)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        student = create_user(db, user_in)
        return student
    except Exception as e:
        print("Signup error:", e)  #print in terminal
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# LOGIN
# ---------------------------

@router.post("/login", response_model=Token)
def login(data: UserLogin = Body(...), db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}

# ---------------------------
# AUTH DEPENDENCY
# ---------------------------

from fastapi import Header

def get_current_student(authorization: str = Header(...), db: Session = Depends(get_db)):
    try:
        # Remove "Bearer " prefix if present
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

    student = get_user_by_email(db, email)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student



# ---------------------------
# PROTECTED ROUTE
# ---------------------------

@router.get("/me", response_model=UserOut)
def get_my_profile(current_student=Depends(get_current_student)):
    return current_student

# ---------------------------
# TEMPORARY DB TEST ROUTE
# ---------------------------

# @router.get("/test_db")
# def test_db(db: Session = Depends(get_db)):

#     """
#     Temporary endpoint to verify database is connected
#     to the backend correctly and working

#     """
#     try:
#         db.execute(text("Select 1"))
#         return {"status": "Database connected successfully!"}
#     except Exception as e:
#         return {"error": str(e)}
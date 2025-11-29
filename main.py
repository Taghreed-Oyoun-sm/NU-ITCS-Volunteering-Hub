from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# Import everything from the shared __init__.py for simplicity
from backend import * from backend.db_connection import SessionLocal 

router = APIRouter(prefix="/students", tags=["students"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 1. Registration Endpoint ---

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def student_register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Registers a new student user."""
    
    # 1. Check if email already exists
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    # 2. Check if student_id already exists (assuming student_id is unique)
    # Note: student_id is PK, so this check isn't strictly necessary before create_user
    # but provides a cleaner error message.
    if db.query(Student).filter(Student.student_id == user_in.student_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID already registered."
        )

    # 3. Create and return the user (password is hashed inside create_user)
    db_user = create_user(db, user_in) # Uses db_operations.py
    return db_user


# --- 2. Login/Token Endpoint ---

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticates user and returns JWT access token."""

    user = get_user_by_email(db, form_data.username) # form_data.username is the email
    
    # 1. Check if user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password): # Uses password_handling.py
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Create JWT token
    # We use the user's email as the subject/identity in the token payload
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token( # Uses JWT_auth.py
        subject=user.email,
        expires_delta=access_token_expires
    )

    # 3. Return the token object
    return {"access_token": access_token, "token_type": "bearer"}
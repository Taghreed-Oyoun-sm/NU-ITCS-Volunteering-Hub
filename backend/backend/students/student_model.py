<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Boolean, Float
=======
from sqlalchemy import Column, Integer, String, Boolean, Float, BIGINT
>>>>>>> 979f903 (Backend and APIS)
from sqlalchemy.orm import relationship
from backend.db_connection import Base

class Student(Base):
<<<<<<< HEAD
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    year = Column(String, nullable=False)
    track = Column(String, nullable=False)
    cgpa = Column(Float, nullable=False)
    research_skills = Column(Boolean, default=False)
    jta_skills = Column(Boolean, default=False)
    
    # ✅ Add this line to match your db_operations
    strength_areas = Column(String, nullable=True) 

    hashed_password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="owner", cascade="all, delete")
=======
    __tablename__ = "Student"

    student_id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    year = Column(String(100), nullable=False)
    track = Column(String(100), nullable=False)
    cgpa = Column(Float, nullable=False)
    # research_skills = Column(Boolean, default=False)
    # jta_skills = Column(Boolean, default=False)
    
    # ✅ Add this line to match your db_operations
    strength_areas = Column(String(500), default="") 

    hashed_password = Column(String(255), nullable=False)

    posts = relationship("Post", back_populates="student")
>>>>>>> 979f903 (Backend and APIS)

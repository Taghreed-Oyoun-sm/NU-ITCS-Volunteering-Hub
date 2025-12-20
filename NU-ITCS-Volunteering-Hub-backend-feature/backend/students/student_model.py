# This file defines the Student table model for SQLAlchemy.
# Each student object represents a row in the Student table in the database.

from sqlalchemy import Column, String, Integer, Float, Boolean, BIGINT
from sqlalchemy.orm import relationship
from backend.db_connection import Base


class Student(Base):
    __tablename__ = "Student"
    
    # Columns definition
    student_id = Column(BIGINT, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index= True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    year = Column(String(50), nullable=False)
    track = Column(String(50), nullable=False)
    cgpa = Column(Float, nullable=False)
    research_skills = Column(Boolean, default=False) 
    jta_skills = Column(Boolean, default=False)
    strength_areas = Column(String, default="")

    # Relationships
    posts = relationship("Post", back_populates="student",cascade="all, delete")
    comments = relationship("Comment", back_populates="student", cascade="all, delete")


    # Notes: 
    
    #deafult=False : if user did not enter a value the default value will be false

    #nullable : column can be empty or not
    #False = must have a value

    #Unique : Two users should not have the same value
    #True = All users have different values
    

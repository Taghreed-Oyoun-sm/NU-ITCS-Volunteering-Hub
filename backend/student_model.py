from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "Student"

    student_id = Column(String(50), primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    year = Column(String(50), nullable=False)
    track = Column(String(50), nullable=False)
    cgpa = Column(Float, nullable=False)
    research_skills = Column(Boolean, default=False)
    jta_skills = Column(Boolean, default=False)

    #deafult=False : if user did not enter a value the default value will be false

    #nullable : column can be empty or not
    #False = must have a value

    #Unique : Two users should not have the same value
    #True = All users have different values
    
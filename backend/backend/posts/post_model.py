from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, BIGINT
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.db_connection import Base

class Post(Base):
    __tablename__ = "posts"

<<<<<<< HEAD
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String, nullable=True)
=======
    post_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(BIGINT, ForeignKey("Student.student_id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(255), nullable=True)
>>>>>>> 979f903 (Backend and APIS)
    
    # Fields used in your db_operations
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)

<<<<<<< HEAD
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False
    )

    owner = relationship("Student", back_populates="posts")
    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete"
    )
=======
    student_id = Column(Integer,ForeignKey("Student.student_id", ondelete="CASCADE"),nullable=False)

    student = relationship("Student", back_populates="posts")
    comments = relationship("Comment",back_populates="post")

    
>>>>>>> 979f903 (Backend and APIS)

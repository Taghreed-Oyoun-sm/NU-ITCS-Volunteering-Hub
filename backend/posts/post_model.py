from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, BIGINT
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.db_connection import Base

class Post(Base):
    __tablename__ = "Post"

    post_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(BIGINT, ForeignKey("Student.student_id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(255), nullable=True)
    
    # Fields used in your db_operations
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)

    student_id = Column(Integer,ForeignKey("Student.student_id", ondelete="CASCADE"),nullable=False)

    student = relationship("Student", back_populates="posts")
    comments = relationship("Comment",back_populates="post")

    
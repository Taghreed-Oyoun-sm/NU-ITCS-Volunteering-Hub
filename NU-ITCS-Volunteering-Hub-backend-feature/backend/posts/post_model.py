from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.db_connection import Base

class Post(Base):
    __tablename__ = "Post"

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(ForeignKey("Student.student_id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String, default="") 
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)


    student = relationship("Student", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)

    post_id = Column(ForeignKey("Post.post_id"), nullable=False)
    student_id = Column(ForeignKey("Student.student_id"), nullable=False)

    post = relationship("Post", back_populates="comments")
    student = relationship("Student", back_populates="comments")

    parent_id = Column(ForeignKey("comments.id"))
    replies = relationship("Comment", cascade="all, delete-orphan")

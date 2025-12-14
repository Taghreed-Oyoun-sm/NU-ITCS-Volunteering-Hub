from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.db_connection import Base
from backend.students.student_model import Student # import for FK reference


class Post(Base):
    __tablename__ = "Post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)  # soft delete flag

    student_id = Column(ForeignKey("Student.student_id"), nullable=False)
    author = relationship("Student", back_populates="posts")

    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy="joined"
    )


class Comment(Base):
    __tablename__ = "Comment"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)  # soft delete flag

    post_id = Column(ForeignKey("Post.id"), nullable=False)
    post = relationship("Post", back_populates="comments")

    student_id = Column(ForeignKey("Student.student_id"), nullable=False)
    author = relationship("Student", back_populates="comments")

    # Threading for unlimited nested replies
    parent_id = Column(ForeignKey("Comment.id"), nullable=True)
    replies = relationship(
        "Comment",
        cascade="all, delete-orphan",
        lazy="joined",
        join_depth=5
    )

class PostReport(Base):
    __tablename__ = "post_reports"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    student_id = Column(Integer)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


class CommentReport(Base):
    __tablename__ = "comment_reports"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    student_id = Column(Integer)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
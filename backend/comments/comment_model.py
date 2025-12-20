from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.db_connection import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    student_id = Column(Integer, ForeignKey("Student.student_id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("Post.post_id", ondelete="CASCADE"), nullable=False)

    post = relationship("Post", back_populates="comments")
    student = relationship("Student")
    parent = relationship("Comment", remote_side=[id], backref="replies")
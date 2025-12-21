import enum
<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from backend.db_connection import Base

=======
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, BIGINT, Text, TIMESTAMP
from sqlalchemy.sql import func
from backend.db_connection import Base


>>>>>>> 979f903 (Backend and APIS)
class TargetType(enum.Enum):
    Student_Question = "post"
    Response = "comment"

class Report(Base):
    __tablename__ = "Report"

<<<<<<< HEAD
    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    # These must match the names used in your db_operations.py
    target_id = Column(Integer, nullable=False) 
    target_type = Column(Enum(TargetType), nullable=False)
    
    reason = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
=======
    Report_ID = Column(BIGINT, primary_key=True, autoincrement=True)
    Post_ID = Column(BIGINT, ForeignKey("Post.post_id"), nullable=False)
    Reporter_Type = Column(Enum("Student", "Doctor", "TA", name="reporter_type_enum"), nullable=False)
    Reporter_ID = Column(BIGINT, nullable=False)
    Reason = Column(Text, nullable=False)
    Report_Time = Column(TIMESTAMP, server_default=func.current_timestamp())
    Status = Column(Enum("Pending", "Reviewed", "Resolved", name="report_status_enum"), server_default="Pending")
>>>>>>> 979f903 (Backend and APIS)

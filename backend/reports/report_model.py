import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, BIGINT, Text, TIMESTAMP
from sqlalchemy.sql import func
from backend.db_connection import Base


class TargetType(enum.Enum):
    Student_Question = "post"
    Response = "comment"

class Report(Base):
    __tablename__ = "Report"

    Report_ID = Column(BIGINT, primary_key=True, autoincrement=True)
    Post_ID = Column(BIGINT, ForeignKey("Post.post_id"), nullable=False)
    Reporter_Type = Column(Enum("Student", "Doctor", "TA", name="reporter_type_enum"), nullable=False)
    Reporter_ID = Column(BIGINT, nullable=False)
    Reason = Column(Text, nullable=False)
    Report_Time = Column(TIMESTAMP, server_default=func.current_timestamp())
    Status = Column(Enum("Pending", "Reviewed", "Resolved", name="report_status_enum"), server_default="Pending")
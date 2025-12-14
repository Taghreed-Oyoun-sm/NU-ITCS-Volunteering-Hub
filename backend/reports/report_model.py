from sqlalchemy import Column, BIGINT, Enum, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.db_connection import Base

class TargetType(str, Enum):
    Student_Question = "Student_Question"
    Response = "Response"

class Report(Base):
    __tablename__ = "Report"

    Report_ID = Column(BIGINT, primary_key=True, autoincrement=True)
    Reporter_ID = Column(BIGINT, nullable=False)
    Target_ID = Column(BIGINT, nullable=False)
    Target_Type = Column(Enum(TargetType), nullable=False)
    Time = Column(DateTime, default=datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint('Reporter_ID', 'Target_ID', 'Target_Type', name='uq_report'),
    )

from enum import Enum
from sqlalchemy import Column, BIGINT, DateTime, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from datetime import datetime, timezone
from backend.db_connection import Base

class TargetType(str, Enum):
    Student_Question = "Student_Question"
    Response = "Response"

class Report(Base):
    __tablename__ = "reports"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    reporter_id = Column(BIGINT, nullable=False)
    target_id = Column(BIGINT, nullable=False)
    target_type = Column(SQLEnum(TargetType), nullable=False)
    time = Column(DateTime, default=datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("reporter_id", "target_id", "target_type", name="uq_report"),
    )

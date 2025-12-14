# backend/reports/db_operations.py
from sqlalchemy.orm import Session
from .report_model import TargetType, Report
from backend.posts.post_model import Post, Comment  # Updated to actual models

REPORT_THRESHOLD = 10

def report_target(db: Session, reporter_id: int, target_id: int, target_type: TargetType):
    # Check if this reporter has already reported this target
    existing = db.query(Report).filter(
        Report.Reporter_ID == reporter_id,
        Report.Target_ID == target_id,
        Report.Target_Type == target_type
    ).first()
    if existing:
        return {"status": "already_reported"}

    # Add the report
    report = Report(
        Reporter_ID=reporter_id,
        Target_ID=target_id,
        Target_Type=target_type
    )
    db.add(report)
    db.commit()

    # Count total reports for this target
    count = db.query(Report).filter(
        Report.Target_ID == target_id,
        Report.Target_Type == target_type
    ).count()

    # If threshold reached, soft-delete the object
    if count >= REPORT_THRESHOLD:
        if target_type == TargetType.Student_Question:
            obj = db.query(Post).filter(Post.id == target_id).first()
        elif target_type == TargetType.Response:
            obj = db.query(Comment).filter(Comment.id == target_id).first()
        else:
            obj = None

        if obj and not obj.is_deleted:
            obj.is_deleted = True
            db.add(obj)
            db.commit()
            return {"status": "deleted", "count": count}

    return {"status": "reported", "count": count}

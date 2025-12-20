from sqlalchemy.orm import Session
from .report_model import TargetType, Report
from backend.posts.post_model import Post
from backend.comments.comment_model import Comment

REPORT_THRESHOLD = 10

def report_target(
    db: Session,
    reporter_id: int,
    target_id: int,
    target_type: TargetType,
    reason: str
):
    # 1. Check if this reporter already reported this target
    existing = db.query(Report).filter(
        Report.Reporter_ID == reporter_id,
        Report.Post_ID == target_id
    ).first()

    if existing:
        return {"status": "already_reported"}

    # 2. Add the report
    report = Report(
        Post_ID=target_id,
        Reporter_ID=reporter_id,
        Reporter_Type="Student",   # fixed value since this API is for students
        Reason=reason
    )
    db.add(report)
    db.commit()

    # 3. Count total reports for this target
    count = db.query(Report).filter(
        Report.Post_ID == target_id
    ).count()

    # 4. If threshold reached, soft-delete
    if count >= REPORT_THRESHOLD:
        obj = None

        if target_type == TargetType.Student_Question:
            obj = db.query(Post).filter(Post.post_id == target_id).first()
        elif target_type == TargetType.Response:
            obj = db.query(Comment).filter(Comment.id == target_id).first()

        if obj and hasattr(obj, "is_deleted") and not obj.is_deleted:
            obj.is_deleted = True
            db.commit()
            return {"status": "deleted", "count": count}

    return {"status": "reported", "count": count}

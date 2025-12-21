from sqlalchemy.orm import Session
from .report_model import TargetType, Report
from backend.posts.post_model import Post
from backend.comments.comment_model import Comment

REPORT_THRESHOLD = 10

<<<<<<< HEAD
def report_target(db: Session, reporter_id: int, target_id: int, target_type: TargetType, reason: str):
    # 1. Check if this reporter has already reported this specific target
    existing = db.query(Report).filter(
        Report.reporter_id == reporter_id,
        Report.target_id == target_id,
        Report.target_type == target_type
    ).first()
    
=======
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

>>>>>>> 979f903 (Backend and APIS)
    if existing:
        return {"status": "already_reported"}

    # 2. Add the report
    report = Report(
<<<<<<< HEAD
        reporter_id=reporter_id,
        target_id=target_id,
        target_type=target_type,
        reason=reason
=======
        Post_ID=target_id,
        Reporter_ID=reporter_id,
        Reporter_Type="Student",   # fixed value since this API is for students
        Reason=reason
>>>>>>> 979f903 (Backend and APIS)
    )
    db.add(report)
    db.commit()

    # 3. Count total reports for this target
    count = db.query(Report).filter(
<<<<<<< HEAD
        Report.target_id == target_id,
        Report.target_type == target_type
    ).count()

    # 4. If threshold reached, soft-delete the object
    if count >= REPORT_THRESHOLD:
        obj = None
=======
        Report.Post_ID == target_id
    ).count()

    # 4. If threshold reached, soft-delete
    if count >= REPORT_THRESHOLD:
        obj = None

>>>>>>> 979f903 (Backend and APIS)
        if target_type == TargetType.Student_Question:
            obj = db.query(Post).filter(Post.post_id == target_id).first()
        elif target_type == TargetType.Response:
            obj = db.query(Comment).filter(Comment.id == target_id).first()

<<<<<<< HEAD
        if obj and hasattr(obj, 'is_deleted') and not obj.is_deleted:
=======
        if obj and hasattr(obj, "is_deleted") and not obj.is_deleted:
>>>>>>> 979f903 (Backend and APIS)
            obj.is_deleted = True
            db.commit()
            return {"status": "deleted", "count": count}

    return {"status": "reported", "count": count}
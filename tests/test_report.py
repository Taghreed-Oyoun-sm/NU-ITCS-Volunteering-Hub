import pytest
from sqlalchemy.orm import Session
from backend.reports.db_operations import report_target, REPORT_THRESHOLD
from backend.reports.report_model import TargetType, Report
from backend.posts.post_model import Post
from backend.students.student_model import Student

def setup_post(db: Session, pid: int):
    student = Student(student_id=pid+500, name="A", email=f"{pid}@n.e", year="J", track="C", cgpa=3.0)
    db.add(student)
    db.flush()
    post = Post(post_id=pid, title="T", content="C", student_id=student.student_id)
    db.add(post)
    db.commit()
    return post

def test_report_post_success(db_session: Session):
    setup_post(db_session, 1)
    
    # Matching your report_target(db, reporter_id, target_id, target_type, reason)
    report_target(db_session, 99, 1, TargetType.Student_Question, "Spam")
    
    report = db_session.query(Report).filter(Report.Post_ID == 1).first()
    assert report is not None
    assert report.Reporter_ID == 99
    assert report.Reason == "Spam"

def test_report_duplicate_prevention(db_session: Session):
    setup_post(db_session, 2)
    report_target(db_session, 88, 2, TargetType.Student_Question, "Reason 1")
    result = report_target(db_session, 88, 2, TargetType.Student_Question, "Reason 2")
    
    assert result["status"] == "already_reported"

def test_soft_delete_at_threshold(db_session: Session):
    post = setup_post(db_session, 3)
    
    for i in range(REPORT_THRESHOLD):
        report_target(db_session, 1000+i, 3, TargetType.Student_Question, "Spam")
    
    db_session.refresh(post)
    assert post.is_deleted is True
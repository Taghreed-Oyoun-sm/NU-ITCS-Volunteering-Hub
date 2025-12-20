import pytest
from sqlalchemy.orm import Session
from backend.reports.db_operations import report_target, REPORT_THRESHOLD
from backend.reports.report_model import TargetType, Report
from backend.posts.post_model import Post
from backend.comments.comment_model import Comment
from backend.students.student_model import Student

# Helper to setup a post so we don't repeat code
def create_test_post(db, post_id):
    # We also need a student because Post depends on Student
    student = Student(student_id=post_id+100, name="Author", email=f"a{post_id}@nu.edu.eg")
    db.add(student)
    post = Post(post_id=post_id, title="Test", content="Content", student_id=student.student_id)
    db.add(post)
    db.commit()
    return post

def test_report_target_success(db_session: Session):
    create_test_post(db_session, 1)
    result = report_target(db_session, 2, 1, TargetType.Student_Question, "Reason")
    assert result["status"] == "reported"

def test_report_target_already_reported(db_session: Session):
    create_test_post(db_session, 1) # MUST setup data again for this test
    report_target(db_session, 2, 1, TargetType.Student_Question, "First")
    result = report_target(db_session, 2, 1, TargetType.Student_Question, "Second")
    assert result["status"] == "already_reported"

def test_report_threshold_soft_delete(db_session: Session):
    post = create_test_post(db_session, 1)
    post.is_deleted = False
    db_session.commit()

    for i in range(1, REPORT_THRESHOLD + 1):
        result = report_target(db_session, 100 + i, 1, TargetType.Student_Question, "Spam")

    assert result["status"] == "deleted"
    db_session.refresh(post)
    assert post.is_deleted is True

def test_report_comment_success(db_session: Session):
    # Setup: Create a student, then a post, then a comment
    create_test_post(db_session, 1)
    comment = Comment(id=1, post_id=1, student_id=101, content="Bad comment")
    db_session.add(comment)
    db_session.commit()

    result = report_target(db_session, 5, 1, TargetType.Response, "Harassment")
    assert result["status"] == "reported"
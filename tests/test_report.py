import pytest
from sqlalchemy.orm import Session
from backend.reports.db_operations import report_target, REPORT_THRESHOLD
from backend.reports.report_model import TargetType, Report
from backend.posts.post_model import Post
from backend.comments.comment_model import Comment
from backend.students.student_model import Student

# Helper to setup a post so we don't repeat code
def create_test_post(db: Session, post_id: int):
    # We MUST create a student first because Post depends on Student (Foreign Key)
    student = Student(
        student_id=post_id + 1000, 
        name=f"Author_{post_id}", 
        email=f"author_{post_id}@nu.edu.eg"
    )
    db.add(student)
    db.flush() # Send to DB so ID is available
    
    post = Post(
        post_id=post_id, 
        title="Test Post", 
        content="Content", 
        student_id=student.student_id,
        is_deleted=False
    )
    db.add(post)
    db.commit()
    return post

# 1. Test basic reporting functionality
def test_report_target_success(db_session: Session):
    create_test_post(db_session, 1) # Setup data
    
    result = report_target(
        db=db_session,
        reporter_id=2,
        target_id=1,
        target_type=TargetType.Student_Question,
        reason="Inappropriate language"
    )

    assert result["status"] == "reported"
    assert result["count"] == 1

# 2. Test prevention of duplicate reports from the same user
def test_report_target_already_reported(db_session: Session):
    create_test_post(db_session, 2) # Fresh post for this test
    
    # Report once
    report_target(db_session, 2, 2, TargetType.Student_Question, "First report")
    
    # Try reporting again
    result = report_target(db_session, 2, 2, TargetType.Student_Question, "Second report")

    assert result["status"] == "already_reported"

# 3. Test soft-deletion after reaching the threshold
def test_report_threshold_soft_delete(db_session: Session):
    post = create_test_post(db_session, 3)
    
    # Simulate multiple unique users reporting
    for i in range(1, REPORT_THRESHOLD + 1):
        result = report_target(
            db=db_session,
            reporter_id=500 + i, 
            target_id=3,
            target_type=TargetType.Student_Question,
            reason="Spam"
        )

    # The last report should trigger deletion
    assert result["status"] == "deleted"
    
    db_session.refresh(post)
    assert post.is_deleted is True

# 4. Test reporting a comment (Response)
def test_report_comment_success(db_session: Session):
    # Setup: Create post first, then a comment on it
    create_test_post(db_session, 4)
    
    comment = Comment(
        id=10, 
        post_id=4, 
        student_id=1001, 
        content="This is a bad comment"
    )
    db_session.add(comment)
    db_session.commit()

    result = report_target(
        db=db_session,
        reporter_id=5,
        target_id=10, # Reporting the comment ID
        target_type=TargetType.Response,
        reason="Harassment"
    )

    assert result["status"] == "reported"
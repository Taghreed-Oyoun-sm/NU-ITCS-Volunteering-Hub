import pytest
from sqlalchemy.orm import Session
from backend.reports.db_operations import report_target, REPORT_THRESHOLD
from backend.reports.report_model import TargetType, Report
from backend.posts.post_model import Post
from backend.comments.comment_model import Comment

# 1. Test basic reporting functionality
def test_report_target_success(db_session: Session):
    # Setup: Create a student and a post first so the IDs exist
    from backend.posts.post_model import Post
    
    # Create the target post
    test_post = Post(
        post_id=1, 
        title="Test Post", 
        content="This is a test", 
        student_id=10, 
        is_deleted=False
    )
    db_session.add(test_post)
    db_session.commit()

    # Now act
    result = report_target(
        db=db_session,
        reporter_id=2, # Ensure this ID exists if there's a FK constraint
        target_id=1,
        target_type=TargetType.Student_Question,
        reason="Inappropriate language"
    )

    assert result["status"] == "reported"
    assert result["count"] == 1
# 2. Test prevention of duplicate reports from the same user
def test_report_target_already_reported(db_session: Session):
    # Setup: Report a target once
    report_target(db_session, 2, 1, TargetType.Student_Question, "First report")
    
    # Try reporting the same target with the same user
    result = report_target(db_session, 2, 1, TargetType.Student_Question, "Second report")

    assert result["status"] == "already_reported"

# 3. Test soft-deletion after reaching the threshold
def test_report_threshold_soft_delete(db_session: Session):
    # Setup: Ensure a post exists that is not yet deleted
    post = db_session.query(Post).filter(Post.id == 1).first()
    post.is_deleted = False
    db_session.commit()

    # Act: Simulate multiple users reporting the post until the threshold is reached
    # We use REPORT_THRESHOLD from your operations file
    for i in range(1, REPORT_THRESHOLD + 1):
        result = report_target(
            db=db_session,
            reporter_id=100 + i, # Unique reporter IDs
            target_id=1,
            target_type=TargetType.Student_Question,
            reason="Spam"
        )

    # Verify the last report triggered the deletion
    assert result["status"] == "deleted"
    
    # Verify the database reflects the soft-delete
    db_session.refresh(post)
    assert post.is_deleted is True

# 4. Test reporting a comment (Response)
def test_report_comment_success(db_session: Session):
    result = report_target(
        db=db_session,
        reporter_id=5,
        target_id=1, # comment_id
        target_type=TargetType.Response,
        reason="Harassment"
    )

    assert result["status"] == "reported"
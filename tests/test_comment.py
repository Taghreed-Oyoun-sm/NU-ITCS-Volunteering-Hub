import pytest
from sqlalchemy.orm import Session
from backend.comments.comment_model import Comment
from backend.comments.comment_dtos import CommentCreate
# Assuming your create function is in db_operations.py
from backend.posts.db_operations import create_comment 

# 1. Test basic comment creation on a post
def test_create_comment_success(db_session: Session):
    # Setup: Assume post_id 1 and student_id 10 exist
    comment_data = CommentCreate(content="This is a very helpful post!", parent_id=None)
    
    result = create_comment(
    db=db_session,
    student_id=10,
    post_id=1,
    content=comment_data.content, # Pass the string inside the object
    parent_id=comment_data.parent_id
    )

    assert result.content == "This is a very helpful post!"
    assert result.post_id == 1
    assert result.student_id == 10
    assert result.parent_id is None

# 2. Test creating a reply to another comment (parent_id)
def test_create_reply_success(db_session: Session):
    # Setup: Create an initial parent comment
    parent = Comment(content="Parent comment", student_id=10, post_id=1)
    db_session.add(parent)
    db_session.commit()
    db_session.refresh(parent)

    # Act: Create a reply linked to that parent_id
    reply_data = CommentCreate(content="I agree with you!", parent_id=parent.id)
    reply = create_comment(
        db=db_session, 
        comment_in=reply_data, 
        student_id=11, 
        post_id=1
    )

    assert reply.parent_id == parent.id
    assert reply.content == "I agree with you!"

# 3. Test that comments are correctly linked to a post
def test_comment_post_relationship(db_session: Session):
    # This verifies the relationship defined in your comment_model.py
    new_comment = Comment(content="Check relationship", student_id=10, post_id=1)
    db_session.add(new_comment)
    db_session.commit()
    
    # Verify the back_populates="comments" link
    assert new_comment.post_id == 1
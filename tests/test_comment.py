import pytest
from sqlalchemy.orm import Session
from backend.posts.db_operations import create_comment
from backend.posts.dtos import CommentCreate
# from backend.posts.comment_model import Comment
from backend.posts.post_model import Post
from backend.students.student_model import Student

def test_create_comment_success(db_session: Session):
    # Setup Foreign Keys
    student = Student(student_id=10, name="User", email="u@nu.edu.eg")
    post = Post(post_id=1, title="T", content="C", student_id=10)
    db_session.add_all([student, post])
    db_session.commit()

    comment_data = CommentCreate(content="This is a very helpful post!", parent_id=None)
    
    result = create_comment(
        db=db_session,
        content=comment_data.content,
        student_id=10,
        post_id=1
    )
    assert result.content == "This is a helpful post!"
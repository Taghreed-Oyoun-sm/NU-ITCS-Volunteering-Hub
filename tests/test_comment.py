import pytest
from sqlalchemy.orm import Session
from backend.posts.db_operations import create_comment
from backend.posts.dtos import CommentCreate
from backend.posts.post_model import Post
from backend.students.student_model import Student

def test_create_comment_success(db_session: Session):
    # 1. Setup Mandatory Foreign Keys
    student = Student(student_id=10, name="User", email="u@nu.edu.eg", year="Junior", track="CS", cgpa=3.5)
    db_session.add(student)
    db_session.flush()

    post = Post(post_id=1, title="Test Post", content="Content", student_id=student.student_id)
    db_session.add(post)
    db_session.commit()

    # 2. Prepare the DTO (Matching your backend logic)
    comment_data = CommentCreate(
        student_id=10,
        post_id=1,
        content="This is a very helpful post!",
        parent_id=None
    )
    
    # 3. Call the function with the DTO object
    result = create_comment(db=db_session, comment_in=comment_data)
    
    assert result.content == "This is a very helpful post!"
    assert result.post_id == 1
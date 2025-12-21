import pytest
from sqlalchemy.orm import Session
from backend.posts.db_operations import create_post, search_posts_by_tag, find_suitable_students, create_comment
from backend.posts.dtos import PostCreate, CommentCreate
from backend.students.student_model import Student
from backend.posts.post_model import Post

# 1. Test Post Creation
def test_create_post_success(db_session: Session):
    student = Student(student_id=1, name="Author", email="a@nu.edu.eg", year="Junior", track="CS", cgpa=3.5)
    db_session.add(student)
    db_session.commit()

    post_data = PostCreate(
        student_id=1,
        title="Python Help",
        content="Looking for help with SQLAlchemy",
        tags=["Python", "Database"]
    )
    
    new_post = create_post(db_session, post_data)

    assert new_post.post_id is not None 
    assert new_post.title == "Python Help"
    assert "Python" in new_post.tags

# 2. Test Searching Posts by Tag
def test_search_posts_by_tag(db_session: Session):
    student = Student(student_id=2, name="Author2", email="a2@nu.edu.eg", year="Senior", track="AI", cgpa=3.5)
    db_session.add(student)
    db_session.flush()

    post_data = PostCreate(student_id=2, title="Math", content="Calculus", tags=["Math"])
    create_post(db_session, post_data)

    results = search_posts_by_tag(db_session, "Math")
    assert len(results) > 0
    assert results[0].title == "Math"

# 3. Test Matching Students by Post Tags
def test_find_suitable_students(db_session: Session):
    student = Student(
        student_id=3,
        name="Expert",
        email="expert@nu.edu.eg",
        year="Junior", track="CS", cgpa=3.5,
        strength_areas="AI, Python"
    )
    db_session.add(student)
    db_session.commit()

    suitable_students = find_suitable_students(db_session, ["AI"])
    assert len(suitable_students) == 1
    assert "AI" in suitable_students[0].strength_areas

# 4. Test Comment Creation (The missing unit test part)
def test_create_comment_success(db_session: Session):
    student = Student(student_id=4, name="User", email="u@nu.edu.eg", year="Junior", track="CS", cgpa=3.5)
    db_session.add(student)
    db_session.flush()
    
    post_obj = Post(post_id=10, title="T", content="C", student_id=4)
    db_session.add(post_obj)
    db_session.commit()

    comment_data = CommentCreate(
        student_id=4,
        post_id=10,
        content="This is a comment",
        parent_id=None
    )
    
    result = create_comment(db_session, comment_data)
    assert result.id is not None
    assert result.content == "This is a comment"
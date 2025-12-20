import pytest
from sqlalchemy.orm import Session
from backend.posts.db_operations import create_post, search_posts_by_tag, find_suitable_students, create_comment
from backend.posts.dtos import PostCreate
from backend.students.student_model import Student

# 1. Test Post Creation
def test_create_post_success(db_session: Session):
    # Prepare data using the DTO
    post_data = PostCreate(
        title="Python Help",
        content="Looking for help with SQLAlchemy",
        tags=["Python", "Database"]
    )
    # We assume a student with ID 1 exists for this test
    # In a real test, you should create the student first
    post_data.student_id = 1 

    new_post = create_post(db_session, post_data)

    assert new_post.id is not None
    assert new_post.title == "Python Help"
    assert "Python,Database" in new_post.tags  # Operations joins tags with commas

# 2. Test Searching Posts by Tag
def test_search_posts_by_tag(db_session: Session):
    # Setup: Create a post with specific tags
    post_data = PostCreate(title="Math", content="Calculus", tags=["Math"])
    post_data.student_id = 1
    create_post(db_session, post_data)

    # Search for the tag
    results = search_posts_by_tag(db_session, "Math")
    
    assert len(results) > 0
    assert results[0].title == "Math"

# 3. Test Matching Students by Post Tags
def test_find_suitable_students(db_session: Session):
    # Setup: Create a student with matching strengths
    student = Student(
        name="Test Student",
        email="test@nu.edu.eg",
        strength_areas="AI, Python"
    )
    db_session.add(student)
    db_session.commit()

    # Search for students who know 'AI'
    suitable_students = find_suitable_students(db_session, ["AI"])

    assert len(suitable_students) == 1
    assert "AI" in suitable_students[0].strength_areas

# 4. Test Comment Creation
def test_create_comment_success(db_session: Session):
    # Note: Requires a valid post_id and student_id
    comment = create_comment(
        db=db_session, 
        student_id=1, 
        post_id=1, 
        content="This is a helpful post!"
    )
    
    assert comment.id is not None
    assert comment.content == "This is a helpful post!"
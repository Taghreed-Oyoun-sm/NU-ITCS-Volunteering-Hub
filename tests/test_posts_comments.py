import pytest
from sqlalchemy.orm import Session
from backend.posts.db_operations import create_post, search_posts_by_tag, find_suitable_students, create_comment
from backend.posts.dtos import PostCreate
from backend.students.student_model import Student
from backend.posts.post_model import Post

# 1. Test Post Creation
def test_create_post_success(db_session: Session):
    # Setup: Create a student first so student_id=1 exists in the DB
    student = Student(
        student_id=1,
        name="Post Author",
        email="author@nu.edu.eg"
    )
    db_session.add(student)
    db_session.commit()

    # Prepare data using the DTO
    post_data = PostCreate(
        title="Python Help",
        content="Looking for help with SQLAlchemy",
        tags=["Python", "Database"]
    )
    
    # Pass student_id directly to the function
    new_post = create_post(db_session, post_data, student_id=1)

    assert new_post.post_id is not None 
    assert new_post.title == "Python Help"
    assert "Python" in new_post.tags

# 2. Test Searching Posts by Tag
def test_search_posts_by_tag(db_session: Session):
    # Setup: Create student and post first
    student = Student(student_id=2, name="Searcher", email="s@nu.edu.eg")
    db_session.add(student)
    db_session.commit()
    
    post_data = PostCreate(title="Math", content="Calculus", tags=["Math"])
    create_post(db_session, post_data, student_id=2)

    # Search for the tag
    results = search_posts_by_tag(db_session, "Math")
    
    assert len(results) > 0
    assert results[0].title == "Math"

# 3. Test Matching Students by Post Tags
def test_find_suitable_students(db_session: Session):
    # Setup: Create student with strength_areas
    student = Student(
        student_id=3,
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
    # Setup: Create student and post required for foreign keys
    student = Student(student_id=4, name="Commenter", email="c@nu.edu.eg")
    db_session.add(student)
    
    # We use post_id=10 to match your Act section
    post = Post(post_id=10, title="Target Post", content="Content", student_id=4)
    db_session.add(post)
    db_session.commit()

    # Act
    comment = create_comment(
        db=db_session, 
        student_id=4, 
        post_id=10, 
        content="This is a helpful post!"
    )
    
    assert comment is not None
    assert comment.content == "This is a helpful post!"
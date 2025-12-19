import pytest
from backend.posts.db_operations import (
    create_post, 
    search_posts_by_tag, 
    find_suitable_students,
    create_comment
)
from backend.posts.dtos import PostCreate, CommentCreate
from backend.students.student_model import Student
from backend.posts.post_model import Post

# --- 1. POST CREATION & SEARCH ---

def test_create_post_success(db_session):
    """Verify post is saved with comma-separated tags."""
    post_in = PostCreate(
        student_id=1,
        title="Calculus Help",
        content="Solving integrals",
        tags=["Math", "Calc"]
    )
    post = create_post(db_session, post_in)
    assert post.post_id is not None
    assert post.tags == "Math,Calc" # Verifies join logic
    assert post.is_deleted is False

def test_search_ignores_deleted_posts(db_session):
    """Ensure soft-deleted posts are filtered out of searches."""
    create_post(db_session, PostCreate(student_id=1, title="Active", content="...", tags=["Search"]))
    deleted = create_post(db_session, PostCreate(student_id=1, title="Hidden", content="...", tags=["Search"]))
    
    deleted.is_deleted = True # Manual soft-delete
    db_session.commit()
    
    results = search_posts_by_tag(db_session, "Search")
    assert len(results) == 1
    assert results[0].title == "Active"

# --- 2. STUDENT MATCHING (PRIORITY LOGIC) ---

def test_match_students_with_messy_spacing(db_session):
    """Verify .strip() handles extra spaces in student strength areas."""
    s1 = Student(student_id=50, strength_areas="  Math  , Physics  ")
    db_session.add(s1)
    db_session.commit()
    
    matches = find_suitable_students(db_session, ["Math"])
    assert len(matches) == 1 # Confirms cleaning logic in db_operations

def test_match_multiple_students_and_tags(db_session):
    """Verify matching logic works for multiple tags simultaneously."""
    s1 = Student(student_id=1, strength_areas="Python")
    s2 = Student(student_id=2, strength_areas="Java")
    db_session.add_all([s1, s2])
    db_session.commit()
    
    matches = find_suitable_students(db_session, ["Python", "Java"])
    assert len(matches) == 2

# --- 3. COMMENTS & REPLIES ---

def test_comment_threading(db_session):
    """Verify that replies are correctly linked to parent comments."""
    # 1. Need a post first
    post = create_post(db_session, PostCreate(student_id=1, title="Q", content="C", tags=[]))
    
    # 2. Create parent comment
    parent = create_comment(db_session, CommentCreate(
        student_id=2, post_id=post.post_id, content="Root comment"
    ))
    
    # 3. Create reply linked via parent_id
    reply = create_comment(db_session, CommentCreate(
        student_id=3, post_id=post.post_id, content="Reply", parent_id=parent.id
    ))
    
    assert reply.parent_id == parent.id # Verifies relationship
    assert reply.post_id == post.post_id
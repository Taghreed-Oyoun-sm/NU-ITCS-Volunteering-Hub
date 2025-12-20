# backend/posts/db_operations.py

from sqlalchemy.orm import Session
from datetime import datetime, timezone
from .post_model import Post
from .dtos import PostCreate, CommentCreate
from backend.comments.comment_model import Comment
from backend.students.student_model import Student


# -------------------- POSTS -------------------- #

def create_post(db: Session, post_in: PostCreate):
    post = Post(
        student_id=post_in.student_id,
        title=post_in.title,
        content=post_in.content,
        tags=",".join(post_in.tags),
        created_at=datetime.now(timezone.utc),
        is_deleted=False
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# -------------------- COMMENTS / REPLIES -------------------- #

# backend/posts/db_operations.py

def create_comment(db: Session, student_id: int, post_id: int, content: str, parent_id: int = None):
    comment = Comment(
        post_id=post_id,
        student_id=student_id,
        content=content,
        parent_id=parent_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# -------------------- SEARCH BY TAG -------------------- #
def search_posts_by_tag(db: Session, tag: str):
    return db.query(Post).filter(
        Post.tags.like(f"%{tag}%"), Post.is_deleted == False
    ).all()


# -------------------- MATCH STUDENTS BY POST TAG -------------------- #
def find_suitable_students(db: Session, post_tags: list[str]):
    # Query all students
    students = db.query(Student).all()
    suitable_students = []

    for student in students:
        # Split strength_areas into list and strip spaces
        student_tags = [tag.strip() for tag in student.strength_areas.split(",")] if student.strength_areas else []
        # Check if any post tag matches student's tags
        if any(tag in student_tags for tag in post_tags):
            suitable_students.append(student)
    return suitable_students

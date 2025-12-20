from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.students.student_model import Student
from backend.students.student_schema import StudentResponse
from backend.posts import db_operations
from backend.comments.comment_model import Comment
from backend.db_connection import SessionLocal
from backend.posts.post_model import Post
from backend.posts.dtos import PostCreate, CommentCreate
from APIs.routers.student_router import get_current_student

router = APIRouter(prefix="/posts", tags=["Posts"])

# ---------------------------
# DB Dependency
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# CREATE POST (AUTH REQUIRED)
# ---------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student)
):
    post = Post(
        title=post_in.title,
        content=post_in.content,     # ✅ MUST match Post model
        tags=",".join(post_in.tags),
        student_id=current_student.student_id    # ✅ CORRECT
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return {
        "message": "Post created successfully",
        "post_id": post.post_id               # ✅ NOT post_id
    }

# ---------------------------
# ADD COMMENT (AUTH REQUIRED)
# ---------------------------
@router.post("/{post_id}/comments")
def add_comment(
    post_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_student=Depends(get_current_student)
):
    post = db.query(Post).filter(
    Post.post_id == post_id
).first()


    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    

    comment = db_operations.create_comment(
    db=db,
    student_id=current_student.student_id,
    post_id=post_id,
    content=comment_in.content,
    parent_id=comment_in.parent_id,
)


    db.add(comment)
    db.commit()
    db.refresh(comment)

    return {
        "message": "Comment added successfully",
        "comment_id": comment.id
    }

# ---------------------------
# SEARCH POSTS BY TAG (PUBLIC)
# ---------------------------
@router.get("/search")
def search_posts(tag: str, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.tags.contains(tag)).all()
    return [
        {
            "post_id": p.post_id,
            "title": p.title,
            "content": p.content,
            "tags": p.tags.split(","),
            "student_id": p.student_id,
            "created_at": p.created_at
        }
        for p in posts
    ]
# APIs/routers/post_router.py


@router.get("/{post_id}/matches", response_model=List[StudentResponse])
def get_matches_for_post(post_id: int, db: Session = Depends(get_db)):
    # 1. Fetch the post
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post or not post.tags:
        return []

    # 2. Extract tags from the post
    post_tags = [t.strip().lower() for t in post.tags.split(",") if t.strip()]

    # 3. Find students whose strength_areas overlap with post_tags
    all_students = db.query(Student).all()
    matched_students = []

    for student in all_students:
        if student.strength_areas:
            # Convert DB string "python,java" to list ["python", "java"]
            student_skills = [s.strip().lower() for s in student.strength_areas.split(",") if s.strip()]
            
            # Check for intersection
            if any(skill in post_tags for skill in student_skills):
                matched_students.append(student)

    return matched_students
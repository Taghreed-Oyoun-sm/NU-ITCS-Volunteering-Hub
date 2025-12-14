# backend/posts/db_operations.py

from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .post_model import Post, Comment
from .dtos import PostCreate, CommentCreate


# -------------------- POSTS -------------------- #

def create_post(db: Session, post_in: PostCreate):
    post = Post(
        student_id=post_in.student_id,
        title=post_in.title,
        content=post_in.content,
        created_at=datetime.now(timezone.utc),
        is_deleted=False
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# -------------------- COMMENTS / REPLIES -------------------- #

def create_comment(db: Session, comment_in: CommentCreate):
    comment = Comment(
        student_id=comment_in.student_id,
        post_id=comment_in.post_id,
        parent_id=comment_in.parent_id,
        content=comment_in.content,
        created_at=datetime.now(timezone.utc),
        is_deleted=False
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

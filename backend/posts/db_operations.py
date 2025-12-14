# backend/posts/db_operations.py

from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .post_model import Post, Comment, PostReport, CommentReport
from .dtos import PostCreate, CommentCreate

REPORT_THRESHOLD = 10


# -------------------- POSTS -------------------- #

def create_post(db: Session, post_in: PostCreate):
    post = Post(
        student_id=post_in.student_id,
        content=post_in.content,
        created_at=datetime.now(timezone.utc),
        is_deleted=False
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def report_post(db: Session, post_id: int, student_id: int):
    """
    Report a post once per student.
    Auto soft-delete when threshold is reached.
    """

    already_reported = db.query(PostReport).filter_by(
        post_id=post_id,
        student_id=student_id
    ).first()

    if already_reported:
        return False

    db.add(PostReport(
        post_id=post_id,
        student_id=student_id,
        created_at=datetime.now(timezone.utc)
    ))
    db.commit()

    reports_count = db.query(PostReport).filter_by(post_id=post_id).count()
    if reports_count >= REPORT_THRESHOLD:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post and not post.is_deleted:
            post.is_deleted = True
            db.commit()
            return True

    return False


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


def report_comment(db: Session, comment_id: int, student_id: int):
    """
    Report a comment once per student.
    Auto soft-delete when threshold is reached.
    """

    already_reported = db.query(CommentReport).filter_by(
        comment_id=comment_id,
        student_id=student_id
    ).first()

    if already_reported:
        return False

    db.add(CommentReport(
        comment_id=comment_id,
        student_id=student_id,
        created_at=datetime.now(timezone.utc)
    ))
    db.commit()

    reports_count = db.query(CommentReport).filter_by(comment_id=comment_id).count()
    if reports_count >= REPORT_THRESHOLD:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if comment and not comment.is_deleted:
            comment.is_deleted = True
            db.commit()
            return True

    return False

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db_connection import get_db
from backend.comments.comment_model import Comment
from backend.comments.comment_schema import CommentCreate, CommentOut
from APIs.routers.student_router import get_current_student

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentOut)
def create_comment(
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_student)
):
    comment = Comment(
        content=data.content,
        post_id=data.post_id,
        parent_id=data.parent_id,
        student_id=current_user.student_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

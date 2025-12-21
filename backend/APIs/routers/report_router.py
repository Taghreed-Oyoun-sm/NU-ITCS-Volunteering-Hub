from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db_connection import get_db
from backend.reports.report_model import TargetType
from backend.reports import db_operations
from backend.reports.report_dtos import ReportCreate
from APIs.routers.student_router import get_current_student

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/")
def create_report(
<<<<<<< HEAD
    data: ReportCreate, 
    db: Session = Depends(get_db), 
    current_student = Depends(get_current_student)
):
    # Determine type
=======
    data: ReportCreate,
    db: Session = Depends(get_db),
    current_student = Depends(get_current_student)
):
    # Determine target type and ID
>>>>>>> 979f903 (Backend and APIS)
    if data.post_id:
        t_type = TargetType.Student_Question
        t_id = data.post_id
    elif data.comment_id:
        t_type = TargetType.Response
        t_id = data.comment_id
    else:
<<<<<<< HEAD
        raise HTTPException(status_code=400, detail="Must provide post_id or comment_id")

    result = db_operations.report_target(
        db=db,
        reporter_id=current_student.id,
=======
        raise HTTPException(
            status_code=400,
            detail="Must provide post_id or comment_id"
        )

    result = db_operations.report_target(
        db=db,
        reporter_id=current_student.student_id,
>>>>>>> 979f903 (Backend and APIS)
        target_id=t_id,
        target_type=t_type,
        reason=data.reason
    )
<<<<<<< HEAD
    return result
=======

    return result
>>>>>>> 979f903 (Backend and APIS)

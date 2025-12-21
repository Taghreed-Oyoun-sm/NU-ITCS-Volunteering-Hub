from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db_connection import engine, Base

<<<<<<< HEAD
# (THIS CREATES TABLES)
from backend.students.student_model import Student
from backend.posts.post_model import Post
from backend.comments.comment_model import Comment
from backend.reports.report_model import Report 
=======
# 🔥 IMPORT MODELS (THIS CREATES TABLES)
from backend.students.student_model import Student
from backend.posts.post_model import Post
from backend.comments.comment_model import Comment
from backend.reports.report_model import Report  # ✅ 1. ADD THIS
>>>>>>> 979f903 (Backend and APIS)

from APIs.routers.student_router import router as student_router
from APIs.routers.post_router import router as post_router
from APIs.routers.comment_router import router as comment_router
<<<<<<< HEAD
from APIs.routers.report_router import router as report_router  
=======
from APIs.routers.report_router import router as report_router  # ✅ 2. ADD THIS
>>>>>>> 979f903 (Backend and APIS)

app = FastAPI(title="NU Volunteering Hub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
# NOW tables will be created
=======
# 🔥 NOW tables will be created
>>>>>>> 979f903 (Backend and APIS)
Base.metadata.create_all(bind=engine)

app.include_router(student_router)
app.include_router(post_router)
app.include_router(comment_router)
<<<<<<< HEAD
app.include_router(report_router) 

@app.get("/")
def root():
    return {"message": "NU Volunteering Hub API is running"}
=======
app.include_router(report_router)  # ✅ 3. ADD THIS

@app.get("/")
def root():
    return {"message": "NU Volunteering Hub API is running"}
>>>>>>> 979f903 (Backend and APIS)

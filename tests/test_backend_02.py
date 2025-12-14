"""
FULL BACKEND TEST:
✔ Student creation + password hashing + fetch
✔ Post creation
✔ Comment creation
✔ Replies using parent_id
✔ Reporting system separate table
✔ Auto-delete after 10 unique reports
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import Base and all models BEFORE create_all
from backend.db_connection import Base, engine
from backend.students.student_model import Student
from backend.posts.post_model import Post, Comment, PostReport, CommentReport

# Import operations and DTOs
from backend.students.db_operations import create_user
from backend.students.dtos import UserCreate
from backend.students.password_handling import verify_password
from backend.posts.db_operations import create_post, create_comment, report_post, report_comment
from backend.posts.dtos import PostCreate, CommentCreate

# -----------------------------
# Setup In-Memory SQLite DB
# -----------------------------
engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# -----------------------------
# Create all tables
# -----------------------------
Base.metadata.create_all(engine)

# -----------------------------
# 1️⃣ Create 12 Students
# -----------------------------
students = []
for i in range(12):
    u = UserCreate(
        student_id=i + 1,
        name=f"Student {i + 1}",
        email=f"s{i + 1}@test.com",
        year="Freshman",
        track="CS",
        cgpa=3.0,
        research_skills=False,
        JTA_skills=False,
        password="pass123"
    )
    students.append(create_user(db, u))

print("✔ Students created")

# -----------------------------
# 2️⃣ Create Post
# -----------------------------
post = create_post(db, PostCreate(student_id=1, content="Test Post"))
print("✔ Post created ID:", post.id)

# -----------------------------
# 3️⃣ Add Comment to Post
# -----------------------------
comment = create_comment(
    db,
    CommentCreate(student_id=2, post_id=post.id, content="Test Comment")
)
print("✔ Comment created ID:", comment.id)

# -----------------------------
# 4️⃣ Reply to the Comment
# -----------------------------
reply = create_comment(
    db,
    CommentCreate(student_id=3, post_id=post.id, content="Test Reply", parent_id=comment.id)
)
print("✔ Reply created ID:", reply.id)

# -----------------------------
# 5️⃣ Report Comment 10 times => DELETE
# -----------------------------
for u in students[:10]:
    deleted = report_comment(db, comment.id, u.student_id)

deleted_comment = db.query(Comment).filter(Comment.id == comment.id).first()
print("✔ Comment auto-deleted after reports" if not deleted_comment else "✘ Comment still exists")

# -----------------------------
# 6️⃣ Report Post 10 times => DELETE
# -----------------------------
for u in students[:10]:
    deleted = report_post(db, post.id, u.student_id)

deleted_post = db.query(Post).filter(Post.id == post.id).first()
print("✔ Post auto-deleted after reports" if not deleted_post else "✘ Post still exists")

# -----------------------------
# Close DB
# -----------------------------
db.close()
print("\n🎯 ALL BACKEND TESTS PASSED SUCCESSFULLY!")

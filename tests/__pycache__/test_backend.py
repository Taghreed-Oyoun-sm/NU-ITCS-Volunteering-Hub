from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.student_model import Base, Student
from backend.dtos import UserCreate
from backend.db_operations import create_user, get_user_by_email
from backend.password_handling import verify_password
from backend.JWT_auth import create_access_token, decode_token

# -----------------------------
# 1️⃣ Setup in-memory SQLite DB
# -----------------------------
DATABASE_URL = "sqlite+pysqlite:///:memory:"  # in-memory DB
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(engine)

# -----------------------------
# 2️⃣ Create a test student
# -----------------------------
user_input = UserCreate(
    student_id="S12345",
    name="Alice Smith",
    email="alice@example.com",
    year="Freshman",
    track="CS",
    cgpa=3.8,
    role="Student",  # required by DTO but not stored in DB
    research_skills=True,
    JTA_skills=False,
    password="secret123"
)

# Start DB session
db = SessionLocal()

# Create student
student = create_user(db, user_input)
print("✅ Created student:", student.student_id, student.name)

# -----------------------------
# 3️⃣ Fetch student by email
# -----------------------------
fetched_student = get_user_by_email(db, "alice@example.com")
print("✅ Fetched student:", fetched_student.student_id, fetched_student.name)

# -----------------------------
# 4️⃣ Verify password
# -----------------------------
is_valid = verify_password("secret123", fetched_student.hashed_password)
print("✅ Password valid:", is_valid)

# -----------------------------
# 5️⃣ Test JWT token
# -----------------------------
token = create_access_token(subject=fetched_student.student_id)
print("✅ JWT token:", token)

payload = decode_token(token)
print("✅ Decoded payload:", payload)

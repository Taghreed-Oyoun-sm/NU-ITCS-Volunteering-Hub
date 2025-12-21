from backend.students.student_model import Student
from backend.students.dtos import UserCreate, UserOut 
from backend.students.db_operations import create_user, get_user_by_email 
from backend.students.password_handling import hash_password, verify_password 
from backend.students.JWT_auth import create_access_token, decode_token
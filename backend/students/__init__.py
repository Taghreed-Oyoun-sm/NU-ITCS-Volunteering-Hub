from backend.student_model import Student
from backend.dtos import UserCreate, UserOut
from backend.db_operations import create_user, get_user_by_email
from backend.password_handling import hash_password, verify_password
from backend.JWT_auth import create_access_token, decode_token

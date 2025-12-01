# tests/test_auth.py
import pytest
from app import sign_up, log_in, users_db

@pytest.fixture(autouse=True)
def clear_db():
    users_db.clear()

def test_sign_up_success():
    result = sign_up("Ali", "1234")
    assert result == "User registered successfully"
    assert "Ali" in users_db

def test_sign_up_existing_username():
    sign_up("Ali", "1234")
    result = sign_up("Ali", "abcd")
    assert result == "Username already exists"

def test_log_in_success():
    sign_up("Sara", "pass")
    result = log_in("Sara", "pass")
    assert result == "Logged in successfully"

def test_log_in_wrong_password():
    sign_up("Sara", "pass")
    result = log_in("Sara", "wrong")
    assert result == "Incorrect password"

def test_log_in_user_not_found():
    result = log_in("NonExistent", "123")
    assert result == "User not found"

# app.py
users_db = {}

def sign_up(username, password):
    if username in users_db:
        return "Username already exists"
    users_db[username] = password
    return "User registered successfully"

def log_in(username, password):
    if username not in users_db:
        return "User not found"
    if users_db[username] != password:
        return "Incorrect password"
    return "Logged in successfully"

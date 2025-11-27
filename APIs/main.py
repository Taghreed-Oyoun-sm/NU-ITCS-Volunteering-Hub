from fastapi import FastAPI
from APIs.routers.student_router import router as student_router
from backend.student_model import Base
from backend.db_connection import engine

app = FastAPI(title="NU Volunteering Hub Students API")

# Create tables
Base.metadata.create_all(bind=engine)

# Add Routers
app.include_router(student_router)

@app.get("/")
def root():
    return {"message": "Students API is running"}

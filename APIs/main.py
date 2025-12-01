# This is the entry point of the FastAPI backend.
# It creates tables, includes routers, and runs the API.

from fastapi import FastAPI
from APIs.routers.student_router import router as student_router
from backend.student_model import Base
from backend.db_connection import engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="NU Volunteering Hub Students API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables in the database
Base.metadata.create_all(bind=engine)

# Add Routers
app.include_router(student_router)

@app.get("/")
def root():
    return {"message": "Students API is running"}

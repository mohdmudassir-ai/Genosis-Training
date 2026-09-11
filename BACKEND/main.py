from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
import os


# =========================================
# LOAD ENVIRONMENT VARIABLES
# =========================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# =========================================
# CHECK ENVIRONMENT VARIABLES
# =========================================

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is not set")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY is not set")


# =========================================
# CREATE SUPABASE CLIENT
# =========================================

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================
# CREATE FASTAPI APP
# =========================================

app = FastAPI(
    title="Genosis Training API",
    description="Student Management Backend API",
    version="1.0.0"
)


# =========================================
# CORS
# =========================================
# Frontend se API ko access karne ke liye

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# HOME ROUTE
# =========================================

@app.get("/")
def home():
    return {
        "message": "FastAPI is running",
        "status": "success"
    }


# =========================================
# HEALTH CHECK
# =========================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# =========================================
# CREATE STUDENT
# =========================================

@app.post("/students")
def create_student(
    name: str,
    course: str,
    marks: int
):

    # Basic validation
    if not name.strip():
        raise HTTPException(
            status_code=400,
            detail="Student name is required"
        )

    if not course.strip():
        raise HTTPException(
            status_code=400,
            detail="Course is required"
        )

    if marks < 0 or marks > 100:
        raise HTTPException(
            status_code=400,
            detail="Marks must be between 0 and 100"
        )

    student = {
        "name": name,
        "course": course,
        "marks": marks
    }

    try:
        response = (
            supabase
            .table("students")
            .insert(student)
            .execute()
        )

        return {
            "message": "Student created successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create student: {str(e)}"
        )


# =========================================
# GET ALL STUDENTS
# =========================================

@app.get("/students")
def get_students():

    try:
        response = (
            supabase
            .table("students")
            .select("*")
            .execute()
        )

        return {
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch students: {str(e)}"
        )


# =========================================
# UPDATE STUDENT
# =========================================

@app.put("/students/{id}")
def update_student(
    id: int,
    name: str,
    course: str,
    marks: int
):

    if id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid student ID"
        )

    if not name.strip():
        raise HTTPException(
            status_code=400,
            detail="Student name is required"
        )

    if not course.strip():
        raise HTTPException(
            status_code=400,
            detail="Course is required"
        )

    if marks < 0 or marks > 100:
        raise HTTPException(
            status_code=400,
            detail="Marks must be between 0 and 100"
        )

    student = {
        "name": name,
        "course": course,
        "marks": marks
    }

    try:
        response = (
            supabase
            .table("students")
            .update(student)
            .eq("id", id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {
            "message": "Student updated successfully",
            "data": response.data
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update student: {str(e)}"
        )


# =========================================
# DELETE STUDENT
# =========================================

@app.delete("/students/{id}")
def delete_student(id: int):

    if id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid student ID"
        )

    try:
        response = (
            supabase
            .table("students")
            .delete()
            .eq("id", id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {
            "message": "Student deleted successfully",
            "data": response.data
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete student: {str(e)}"
        )
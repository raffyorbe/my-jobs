from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from models import JobCreate, JobUpdate, JobsListResponse
from models_db import Job
from utils import find_job, success_response, error_response
from database import sessionLocal # Import from database.py
from sqlalchemy.orm import Session
from services.job_service import get_all_jobs, get_job, create_job, update_job, delete_job

router = APIRouter()

# Database
def get_db():
    db = sessionLocal() # manages the DB connection/session
    try:
        yield db
    finally:
        db.close()

# READ all
@router.get("/jobs")
def get_jobs_route(
    db: Session = Depends(get_db), # uses resulting db session into endpoint automatically
    completed: Optional[bool] = Query(default=None),
    title: Optional[str] = Query(default=None),
    skip: int = Query(default=0), # how many records to skip
    limit: int = Query(default=10), # how many records to return
    sort: Optional[str] = Query(default=None), #what value to use for sorting
    order: Optional[str] = Query(default="asc"), #ascending or descending order for sorting
):
    
    jobs = get_all_jobs(db, completed, title, skip, limit, sort, order)
    return success_response(jobs)

# READ id
@router.get("/jobs/{job_id}")
def get_job_route(job_id: int, db: Session = Depends(get_db)): 
    job = get_job(job_id, db) #Access db.query(Job) table, find the rows where Job.id (in table) is same as job_id (input) - return only one item first() instead of a list all()
    if not job:
        return error_response(404, "Job not found")
    return success_response(job)

# CREATE
@router.post("/jobs") 
def create_job_route(job: JobCreate, db: Session = Depends(get_db)): # This will shift back to include job: JobCreate because frontend sends JSON with data structure, not individual query paramaeters title completed etc.
    new_job = create_job(job, db)
    return success_response(new_job, "Job created successfully")

# UPDATE
@router.put("/jobs/{job_id}")
def update_job_route(job_id: int, job: JobUpdate, db: Session = Depends(get_db)): 
    job = update_job(job_id, job, db)
    if not job:
        return error_response(404, "Job not found")
    return success_response(job)

# DELETE
@router.delete("/jobs/{job_id}")
def delete_job_route(job_id: int, db: Session = Depends(get_db)):
    job = delete_job(job_id, db)
    if not job:
        return error_response(404, "Job not found")
    return success_response(job, "Job deleted successfully")
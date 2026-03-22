from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from models import JobCreate, JobResponse, JobsListResponse
from models_db import Job
from utils import find_job
from database import sessionLocal # Import from database.py
from sqlalchemy.orm import Session

router = APIRouter()


# Database
# jobs = []
def get_db():
    db = sessionLocal() # db will replace jobs = [] once declared as jobs in endpoint
    try:
        yield db
    finally:
        db.close()


# READ all
@router.get("/jobs") #response model also removed since this is now done by models_db.py
def get_jobs(
    db: Session = Depends(get_db),
):
    jobs = db.query(Job).all()
    
    return jobs

# # READ id
# @router.get("/jobs/{job_id}", response_model=JobResponse) # Dynamic path
# def get_job(job_id: int): # Extract job_id from url and assign as integer
#     index = find_job(job_id, jobs)
#     if index is None:
#         raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
#     return jobs[index]

# # CREATE
# @router.post("/jobs", response_model=JobResponse) # response_model tells function to return following jobResponse model
# def create_job(job: JobCreate): # Create job as JobCreate data type then run function.
#     if any(j.id == job.id for j in jobs):
#         raise HTTPException(status_code=400, detail=f"Job with id {job.id} already exists")
#     if not job.title.strip():
#         raise HTTPException(status_code=422, detail="Title cannot be empty")
#     jobs.append(job) # Append job to jobs list in memory
#     return job

# # UPDATE
# @router.put("/jobs/{job_id}", response_model=JobResponse)
# def update_job(job_id: int, updated_job: JobCreate): # Extract job_id from url and assign as integer AND take job data input and set as updated_job
#     index = find_job(job_id, jobs)
#     if index is None:
#         raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
#     jobs[index] = updated_job # Updates original job item (updated_job)
#     return jobs[index]

# # DELETE
# @router.delete("/jobs/{job_id}")
# def delete_job(job_id: int):
#     index = find_job(job_id, jobs)
#     if index is None:
#         raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
#     deleted = jobs.pop(index) 
#     return {"detail": f"Job {deleted.id} deleted"}
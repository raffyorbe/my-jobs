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
    db = sessionLocal() # manages the DB connection/session
    try:
        yield db
    finally:
        db.close()


# READ all
@router.get("/jobs")
def get_jobs(
    db: Session = Depends(get_db), # uses resulting db session into endpoint automatically

    completed: Optional[bool] = Query(default=None),
    title: Optional[str] = Query(default=None),
    skip: int = Query(default=0), # how many records to skip
    limit: int = Query(default=10), # how many records to return
    sort: Optional[str] = Query(default=None), #what value to use for sorting
    order: Optional[str] = Query(default="asc"), #ascending or descending order for sorting
):
    # jobs = db.query(Job).all()
    query = db.query(Job)

    # Step 1 - FILTER
    if completed is not None:
        query = query.filter(Job.completed == completed)

    if title is not None:
        query = query.filter(Job.title.ilike(f"%{title}%"))

    # Step 2 - SORT
    descending = (order or "asc").lower() == "desc" # Bool 1 if == "desc"

    if sort:
        column = getattr(Job, sort, None) # Get column within the Job model that matches whatever the value of sort is. Else, none (in case sort value is ivalid).
        if column is not None:
            if descending: # If bool descending is 1
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
    
    total = query.count() # Total of all filtered results - not after paginating which only returns total on the page

    # Step 3 - PAGINATE
    results =  query.offset(skip).limit(limit).all() # offset(skip) - start at index [skip]; limit(limit) - limit to (limit) number of rows
    
    return {
        "total": total,
        "count": len(results),
        "data": results
        }

# # READ id
# @router.get("/jobs/{job_id}")
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
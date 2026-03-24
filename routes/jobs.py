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
    results =  query.offset(skip).limit(limit).all() # offset(skip) - start at index [skip]; limit(limit) - limit to (limit) number of rows; all() gets everything w/ or w/o filter sort paginate conditions
    
    return {
        "total": total,
        "count": len(results),
        "data": results
        }

# READ id
@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)): 
    job = db.query(Job).filter(Job.id == job_id).first() #Access db.query(Job) table, find the rows where Job.id (in table) is same as job_id (input) - return only one item first() instead of a list all()
    if not job:
        return {"error": "Job not found"} # Always {"key": "value"}
    return job

# CREATE
@router.post("/jobs") 
def create_job(title: str, completed: bool, db: Session = Depends(get_db)): # This will shift back to include job: JobCreate because frontend sends JSON with data structure, not individual query paramaeters title completed etc.
    new_job = Job(title = title, completed = completed) # in Job, title takes title (str) and completed takes completed (bool)
    db.add(new_job) # Add new_job entry into db
    db.commit() # Save the entry
    db.refresh(new_job) # Pulls the latest data from db which might include auto generated id number
    return new_job

# UPDATE
@router.put("/jobs/{job_id}")
def update_job(job_id: int, title: str, completed: bool, db: Session = Depends(get_db)): 
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return {"error": "Job not found"}
    job.title = title # Ignore error in syntax in IDE because at runtime, job will already exist
    job.completed = completed
    db.commit()
    db.refresh(job)
    return job

# DELETE
@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return {"error": "Job not found"}
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}
from sqlalchemy.orm import Session
from models_db import Job
from models import JobCreate, JobUpdate
from typing import Optional

# READ ALL
def get_all_jobs(
    db: Session,
    completed: Optional[bool] = None,
    title: Optional[str] = None,
    skip: int = 0, # how many records to skip
    limit: int = 10, # how many records to return
    sort: Optional[str] = None, #what value to use for sorting
    order: Optional[str] ="asc", #ascending or descending order for sorting
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

# READ ID
def get_job(
    job_id: int,
    db: Session
):
    return db.query(Job).filter(Job.id == job_id).first()

# CREATE
def create_job(job: JobCreate, db: Session):
    new_job = Job(title = job.title, completed = job.completed) # in Job, title takes title (str) and completed takes completed (bool)
    db.add(new_job) # Add new_job entry into db
    db.commit() # Save the entry
    db.refresh(new_job) # Pulls the latest data from db which might include auto generated id number
    return new_job

# UPDATE
def update_job(job_id: int, job: JobUpdate, db: Session):
    job_update = db.query(Job).filter(Job.id == job_id).first()
    if not job_update:
        return None
    job_update.title = job.title # Ignore error in syntax in IDE because at runtime, job will already exist
    job_update.completed = job.completed
    db.commit()
    db.refresh(job_update)
    return job_update

# DELETE
def delete_job(job_id: int, db: Session):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return None
    db.delete(job)
    db.commit()
    return job
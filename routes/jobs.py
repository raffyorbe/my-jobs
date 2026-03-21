from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models import JobCreate, JobResponse, JobsListResponse
from utils import find_job

router = APIRouter()

jobs = []

# READ all
@router.get("/jobs", response_model = JobsListResponse)
def get_jobs( # These are the "inputs"
    completed: Optional[bool] = Query(default=None),
    title: Optional[str] = Query(default=None),
    skip: int = Query(default=0), # how many records to skip
    limit: int = Query(default=10), # how many records to return - "show x items" toggle
    sort: Optional[str] = Query(default=None), #what value to use for sorting
    order: Optional[str] = Query(default="asc"), #ascending or descending order for sorting
):
    results = jobs.copy() # Duplicate the database to create a per user filter/sort/paginate request, otherwise it applies to the original database
    descending = (order or "asc").lower() == "desc" # Logical order == "desc" -> True if "desc"; If order exists, use it. Else, default to asc. Lower it and then check for condition.

    # Step 1 - FILTER
    if completed is not None:
        results = [job for job in results if job.completed == completed]

    if title is not None:
        results = [job for job in results if title.lower() in job.title.lower()] # title.lower() IN -> ignores case sensitivity of logical == which forces exact match

    total = len(results) # Count the total filtered

    # Step 2 - SORT
    if sort:
        try:
            results = sorted(results, key=lambda job: getattr(job, sort), reverse=descending) # getattr dynamically accesses the property (job.value_of_sort); reverse = bool True or False
        except AttributeError:
            pass

    # Step 3 - PAGINATE
    paginated = results[skip: skip + limit]
    
    return {
        "total": total,
        "count": len(paginated),
        "data": paginated
    }

# READ id
@router.get("/jobs/{job_id}", response_model=JobResponse) # Dynamic path
def get_job(job_id: int): # Extract job_id from url and assign as integer
    index = find_job(job_id, jobs)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return jobs[index]

# CREATE
@router.post("/jobs", response_model=JobResponse) # response_model tells function to return following jobResponse model
def create_job(job: JobCreate): # Create job as JobCreate data type then run function.
    if any(j.id == job.id for j in jobs):
        raise HTTPException(status_code=400, detail=f"Job with id {job.id} already exists")
    if not job.title.strip():
        raise HTTPException(status_code=422, detail="Title cannot be empty")
    jobs.append(job) # Append job to jobs list in memory
    return job

# UPDATE
@router.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(job_id: int, updated_job: JobCreate): # Extract job_id from url and assign as integer AND take job data input and set as updated_job
    index = find_job(job_id, jobs)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    jobs[index] = updated_job # Updates original job item (updated_job)
    return jobs[index]

# DELETE
@router.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    index = find_job(job_id, jobs)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    deleted = jobs.pop(index) 
    return {"detail": f"Job {deleted.id} deleted"}
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models import JobCreate, JobResponse
from utils import find_job

router = APIRouter()

jobs = []

@router.get("/jobs", response_model=list[JobResponse])
def get_jobs( # These are the "inputs"
    completed: Optional[bool] = Query(default=None),
    title: Optional[str] = Query(default=None),
    skip: int = Query(default=0), # how many records to skip
    limit: int = Query(default=10), # how many records to return
    sort: Optional[str] = Query(default=None), #what value to use for sorting
    order: Optional[str] = Query(default="asc"), #ascending or descending order for sorting
):
    results = jobs
    descending = order == "desc"

    # Step 1 - FILTER
    if completed is not None:
        results = [job for job in results if job.completed == completed]

    if title is not None:
        results = [job for job in results if title.lower() == job.title.lower()]

    # Step 2 - SORT
    if sort == "title":
        results = sorted(results, key=lambda job: job.title, reverse=descending)

    if sort == "completed":
        results = sorted(results, key=lambda job: job.completed, reverse=descending)

    # Step 3 - PAGINATE
    return results[skip: skip + limit]

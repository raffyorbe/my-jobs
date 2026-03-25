from fastapi import HTTPException
from typing import List, Optional
from models import JobCreate

# Finder
def find_job(job_id: int, jobs: List[JobCreate]) -> Optional[int]:
    for index, job in enumerate(jobs):     # Return the index of the job in the list, or None if not found
        if job.id == job_id:
            return index
    return None

# Success message
def success_response(data, message="Success"):
    return {
        "success": True,
        "data": data,
        "message": message
    }

# Error message
def error_response(status_code: int, message: str):
    raise HTTPException(
        status_code=status_code,
        detail={
            "success": False,
            "message": message
        }
    )
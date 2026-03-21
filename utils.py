from typing import List, Optional
from models import JobCreate

def find_job(job_id: int, jobs: List[JobCreate]) -> Optional[int]:
    for index, job in enumerate(jobs):     # Return the index of the job in the list, or None if not found
        if job.id == job_id:
            return index
    return None
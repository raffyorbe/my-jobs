from fastapi import FastAPI, HTTPException, Query # Bring in the FastAPI and HTTPException classes
from typing import Optional
from models import JobCreate, JobResponse # Imports models from models.py -  from filename import modelname, from directory.filename if inside subfolder
from fastapi.middleware.cors import CORSMiddleware # CORS
from utils import find_job


app = FastAPI() # Create web app instance. This is the API app

# -------- React frontend connection --------
origins = [
    "http://localhost:3000",  # React server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # what domains can talk to this API
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, PUT, DELETE - All *
    allow_headers=["*"],    # All JSON and auth headers
)

# -------- Database --------
jobs = [] 

@app.get("/") # When browser runs 127.0.0.1:8000/, run the function below.
def read_root(): # Function
    return {"message": "API is running"} # Output of the function

# -------- Read job list --------
@app.get("/jobs", response_model=list[JobResponse]) # list each job following jobResponse format
def get_jobs(
    completed: Optional[bool] = Query(default=None),
    title: Optional[str] = Query(default=None)
):
    results = jobs 

    if completed is not None: # Filter by status
        results = [job for job in results if job.completed == completed]

    if title is not None: #Filter by name (search function)
        results = [job for job in results if title.lower() in job.title.lower()]

    # results takes all job entries [] in jobs[] that meet the filtering condition
    
    return results # Returns list of jobs (filtered)

# -------- Read single job --------
@app.get("/jobs/{job_id}", response_model=JobResponse) # Dynamic path
def get_job(job_id: int): # Extract job_id from url and assign as integer
    index = find_job(job_id, jobs)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found") # Else (after loop), raise HTTP Exception
    return jobs[index]

# -------- Create job --------
@app.post("/jobs", response_model=JobResponse) # response_model tells function to return following jobResponse model
def create_job(job: JobCreate): # Create job as jobCreate data type then run function.
    if any(j.id == job.id for j in jobs):
        raise HTTPException(status_code=400, detail=f"Job with id {job.id} already exists")
    if not job.title.strip():
        raise HTTPException(status_code=422, detail="Title cannot be empty")
    jobs.append(job) # Append job to jobs list in memory
    return job 

# -------- Update job --------
@app.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(job_id: int, updated_job: JobCreate): # Extract job_id from url and assign as integer AND take job data input and set as updated_job
    index = find_job(job_id, jobs)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    jobs[index] = updated_job # Updates original job item (updated_job)
    return jobs[index]

# -------- Delete job --------
@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    index = find_job(job_id, jobs)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    deleted = jobs.pop(index) 
    return {"detail": f"Job {deleted.id} deleted"}

    
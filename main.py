from fastapi import FastAPI, HTTPException, Query # Bring in the FastAPI and HTTPException classes
from typing import Optional
from models import JobCreate, JobResponse # Imports models from models.py -  from filename import modelname, from directory.filename if inside subfolder
from routes.jobs import router as jobs_router# From routes/jobs.py, import a router as jobs_router
from fastapi.middleware.cors import CORSMiddleware # CORS
from utils import find_job


app = FastAPI() # Create web app instance. This is the API app
app.include_router(jobs_router) # Add router from routes/job.py

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
# Transferred to jobs_router jobs.py

# -------- Read single job --------
@app.get("/jobs/{job_id}", response_model=JobResponse) # Dynamic path
def get_job(job_id: int): # Extract job_id from url and assign as integer
    index = find_job(job_id, jobs)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found") # Else (after loop), raise HTTP Exception
    return jobs[index]


# -------- Create job --------
@app.post("/jobs", response_model=JobResponse) # response_model tells function to return following jobResponse model
def create_job(job: JobCreate): # Create job as JobCreate data type then run function.
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

    
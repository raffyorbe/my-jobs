from fastapi import FastAPI, HTTPException, Query # Bring in the FastAPI and HTTPException classes
from typing import Optional
from models import JobCreate, JobResponse # Imports models from models.py -  from filename import modelname, from directory.filename if inside subfolder
from routes.jobs import router as jobs_router# From routes/jobs.py, import a router as jobs_router
from fastapi.middleware.cors import CORSMiddleware # CORS
from utils import find_job
from database import engine
from models_db import Job


app = FastAPI() # Create web app instance. This is the API app
app.include_router(jobs_router) # Add router from routes/job.py
Job.metadata.create_all(bind=engine) #Create DB table

# -------- React frontend connection --------
origins = [
    "http://localhost:3000",  # React server (local)
    "http://localhost:5173", # Vite port (local)
    "http://raffyorbe.github.io" # GitHub Pages
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # what domains can talk to this API
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, PUT, DELETE - All *
    allow_headers=["*"],    # All JSON and auth headers
)

# -------- Database --------
# jobs_router jobs.py 

@app.get("/") # When browser runs 127.0.0.1:8000/, run the function below.
def read_root(): # Function
    return {"message": "API is running"} # Output of the function

# -------- Read job list --------
# jobs_router jobs.py

# -------- Read single job --------
# jobs_router jobs.py

# -------- Create job --------
# jobs_router jobs.py


# -------- Update job --------
# jobs_router jobs.py

# -------- Delete job --------
# jobs_router jobs.py

# Uvicorn startup block
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)

    
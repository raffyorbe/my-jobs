from pydantic import BaseModel # Bring in the Pydantic class to use as BaseModel (removes manual parsing, validation, error handling)
from typing import List

# -------- Todo data model --------
class JobCreate(BaseModel): # Input model
    id: int
    title: str
    completed: bool = False

class JobResponse(BaseModel): # Output model
    id: int
    title: str
    completed: bool

class JobsListResponse(BaseModel):
    total: int
    count: int
    data: List[JobResponse]
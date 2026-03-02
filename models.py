from pydantic import BaseModel # Bring in the Pydantic class to use as BaseModel (removes manual parsing, validation, error handling)

# -------- Todo data model --------
class TodoCreate(BaseModel): # Input model
    id: int
    title: str
    completed: bool = False

class TodoResponse(BaseModel): # Output model
    id: int
    title: str
    completed: bool
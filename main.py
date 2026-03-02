from fastapi import FastAPI, HTTPException # Bring in the FastAPI and HTTPException classes
from models import TodoCreate, TodoResponse # Imports models from models.py -  from filename import modelname, from directory.filename if inside subfolder
from fastapi.middleware.cors import CORSMiddleware # CORS
from utils import find_todo


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
todos = [] 

@app.get("/") # When browser runs 127.0.0.1:8000/, run the function below.
def read_root(): # Function
    return {"message": "API is running"} # Output of the function

# -------- Read todo list --------
@app.get("/todos", response_model=list[TodoResponse]) # list each todo following TodoResponse format
def get_todos():
    return todos # Returns list of todos

# -------- Read single todo --------
@app.get("/todos/{todo_id}", response_model=TodoResponse) # Dynamic path
def get_todo(todo_id: int): # Extract todo_id from url and assign as integer
    index = find_todo(todo_id, todos)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found") # Else (after loop), raise HTTP Exception
    return todos[index]

# -------- Create todo --------
@app.post("/todos", response_model=TodoResponse) # response_model tells function to return following TodoResponse model
def create_todo(todo: TodoCreate): # Create todo as TodoCreate data type then run function.
    if any(t.id == todo.id for t in todos):
        raise HTTPException(status_code=400, detail=f"Todo with id {todo.id} already exists")
    if not todo.title.strip():
        raise HTTPException(status_code=422, detail="Title cannot be empty")
    todos.append(todo) # Append todo to todos list in memory
    return todo 

# -------- Update todo --------
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, updated_todo: TodoCreate): # Extract todo_id from url and assign as integer AND take Todo data input and set as updated_todo
    index = find_todo(todo_id, todos)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    todos[index] = updated_todo # Updates original todo item (updated_todo)
    return todos[index]

# -------- Delete todo --------
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    index = find_todo(todo_id, todos)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    deleted = todos.pop(index) 
    return {"detail": f"Todo {deleted.id} deleted"}

    
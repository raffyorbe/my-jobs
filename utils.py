from typing import List, Optional
from models import TodoCreate

def find_todo(todo_id: int, todos: List[TodoCreate]) -> Optional[int]:
    # Return the index of the todo in the list, or None if not found
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            return index
    return None
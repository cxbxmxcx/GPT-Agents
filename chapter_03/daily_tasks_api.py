from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define a Pydantic model for a task
class Task(BaseModel):
    id: int
    description: str
    completed: bool

# Mock data: List of tasks
tasks = [
    Task(id=1, description="Buy groceries", completed=False),
    Task(id=2, description="Read a book", completed=True),
    Task(id=3, description="Complete FastAPI project", completed=False),
]

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """
    Retrieve a list of daily tasks.
    """
    return tasks

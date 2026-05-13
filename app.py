from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()

# Add CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory storage for simplicity
todos_db = []

class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: str = None
    completed: bool = None

class TodoItem(BaseModel):
    id: str
    title: str
    completed: bool

@app.get("/")
async def root():
    return {"message": "Todo API is running at /api/todos"}

@app.get("/api/todos", response_model=List[TodoItem])
async def get_todos():
    return todos_db

@app.post("/api/todos", response_model=TodoItem)
async def create_todo(todo: TodoCreate):
    new_todo = TodoItem(
        id=str(uuid.uuid4()),
        title=todo.title,
        completed=False
    )
    todos_db.append(new_todo)
    return new_todo

@app.put("/api/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    for todo in todos_db:
        if todo.id == todo_id:
            if todo_update.title is not None:
                todo.title = todo_update.title
            if todo_update.completed is not None:
                todo.completed = todo_update.completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: str):
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            del todos_db[i]
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
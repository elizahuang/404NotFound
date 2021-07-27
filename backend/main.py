from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import numpy
import pandas
import matplotlib

import tensorflow
import os
from model import Todo

from controller import fetch_one_todo, fetch_all_todos, create_todo, update_todo, remove_todo


from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root_page():
    return """<html>
        <head>
            <title>TODO List</title>
        </head>
        <body>
            <h1>Hello TODO List</h1>
        </body>
    </html>"""


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response


@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_title(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.post("/api/todo/", response_model=Todo)
async def post_todo(todo: Todo):
    print(f'post body: {todo.dict()}')
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Please check with server or post body.")


@app.put("/api/todo/{title}/", response_model=Todo)
async def put_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {title}")

import motor.motor_asyncio
from model import Todo
from fastapi.encoders import jsonable_encoder

client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb+srv://admin:admin@cluster0.gitsk.mongodb.net/myFirstDatabase?retryWrites=true')
# mongodb://root:root@localhost:27017/
database = client.myFirstDatabase
# TodoList

collection = database.todo


# async def fetch_user_todo(todo_name):
#     document = await collection.find_one({"todo_name": todo_name})
#     return document

async def fetch_user_todo(user_id):
    document = await collection.find({"user_id": user_id})
    return document

async def fetch_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos


async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document


async def update_todo(todo_name, payload):
    await collection.update_one({"todo_name": todo_name}, {"$set": payload})
    document = await collection.find_one({"todo_name": todo_name})
    return document


async def remove_todo(todo_name):
    await collection.delete_one({"todo_name": todo_name})
    return True

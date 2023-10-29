from enum import Enum
from typing import Union
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

class Program(str, Enum):
    java = "Java"
    javascript = "Javascript"
    php = "PHP"
    python = "Python"

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: limit]

# NOTE オプショナルなパラメータはデフォルト値をNoneとして表現する
# https://fastapi.tiangolo.com/ja/tutorial/query-params/#_3
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/programs/{program_id}")
async def read_program(program_id: Program):
    if program_id is Program.java:
        return {"message": "Java Program"}
    elif program_id is Program.javascript:
        return {"message": "Javascript Program"}
    elif program_id is Program.php:
        return {"message": "PHP Program"}
    elif program_id is Program.python:
        return {"message": "Python Program"}
    else:
        return {"program_id": program_id}
    
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        total = item.price + item.tax
        item_dict.update({"total": total})
    return item_dict
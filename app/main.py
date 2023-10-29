from enum import Enum
from typing import Annotated, List, Union
from pydantic import BaseModel

from fastapi import FastAPI, Path, Query

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

# NOTE Queryで追加バリデーションの定義などが可能、またList型を引数とすることで複数の値を持つこともできる
# https://fastapi.tiangolo.com/ja/tutorial/query-params-str-validations/#_2
# https://fastapi.tiangolo.com/ja/tutorial/query-params-str-validations/#_7
@app.get("/items/search")
def search_items(
    q: List[str] = Query(
        title = "検索クエリ", # docs用のタイトル
        description = "検索用のクエリパラメータ", # docs用の説明文
        default = [],
        max_length = 50,

    )
):
    return {"q": q}

# NOTE オプショナルなパラメータはデフォルト値をNoneとして表現する
# https://fastapi.tiangolo.com/ja/tutorial/query-params/#_3
@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(title="The ID of the item to get", default=None, gt=0, le=1000),
    q: Union[str, None] = None
):
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
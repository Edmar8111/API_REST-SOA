from enum import Enum
from typing import Annotated, Union
from pydantic import BaseModel, AfterValidator
from fastapi import FastAPI, Query
from random import choice

data={
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id:str):
    if not id.startswith(("isbn-","imdb-")):
        raise ValueError("Invalid ID format, it must start with 'isbn-' or 'imdb-' ")
    return id

class ModelName(str, Enum):
    alexnet="alexnext"
    resnet="resnet"
    lenet="lenet"

class Item(BaseModel):
    name:str
    description:str | None = None
    price: float
    tax: float | None = None

fake_items_db=[{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}]


app=FastAPI()

@app.get("/", include_in_schema=False) # -> False define não visivel a rota
async def root():
    return {"message":"Hello World"}

@app.get("/items/{item_id}/", include_in_schema=False)
async def read_item(
        item_id:int|str, q:str | None=None, short: bool=False, skip:int=0, limit:int|None=None
    ): # -> leitura de dado unico com consulta
    item={"item_id":item_id, "skip":skip, "limit":limit}
    if q:
        return {"item_id":item_id, "q":q}
    if not short:
        item.update(
            {"descripton":"This is an amazing item that has a long description"}
        )
    return item

@app.post("/item/create/", include_in_schema=False)
async def create_item(
        item:Item
    ):
    item_dict=item.model_dump()
    if item.tax is not None:
        price_with_tax=item.price+item.tax
        item_dict.update({"price_with_tax":price_with_tax})
    print(item_dict)
    return item_dict

@app.put("/items/update/{item_id}", include_in_schema=False)
async def update_item(
        item_id:int, item:Item, q: Annotated[str | None, Query(max_length=50)]=None
    ):
    result={"item_id":item_id, **item.model_dump()}
    if q:
        result.update({"q":q})
    return result

@app.get("/item/listagem/", include_in_schema=False)
async def read_list_item(
        q: Annotated[list[str] | None, Query()]=None
    ):
    query_items={"q":q}

    return query_items


@app.get("/user/{user_id}/items/{item_id}/", include_in_schema=False)
async def read_user_item(
        user_id:int, item_id:str, q: str|None = Query(default=None, min_length=3, max_length=50, pattern="^fixedquery$"), short:bool=False
    ):
    item={"item_id":item_id, "owner_id":user_id}
    if q:
        item.update({"q":q})
        if not short:
            item.update(
                {"description":"This is an amazing item that has a long description"}
            )
    return item

@app.get("/items/", include_in_schema=False)
async def read_items(
        skip: int=0, limit: int=10
    ): # -> leitura de dados via paginação
    return fake_items_db[skip : skip+limit]

@app.get("/models/{model_name}/", include_in_schema=False)
async def get_model(
        model_name: ModelName
    ):
    if model_name is ModelName.alexnet:
        return {"model_name":model_name, "message":"Depp Learning FTW!"}
    if model_name.value=="lenet":
        return {"model_name":model_name, "message":"leCNN all the images"}
    
    return {"model_name":model_name, "message":"Have some residuals"}

@app.get("/files/{file_path:path}/", include_in_schema=False)
async def read_file(
        file_path:str
    ):
    return {"file_path":file_path}


@app.get("/items_new/")
async def read_items(
    q: Annotated[str | None, Query(title="Query string",description="This is an description return", min_length=3, alias="item-query", deprecated=False, include_in_schema=False)]=None
):
    results={"items":[{"item_id":"Foo"},{"item_id":"Bar"}]}
    if q:
        results.update({"q":q})
    return results

@app.get("/item_validate/")
async def read_item(
    id:Annotated[str|None, AfterValidator(check_valid_id)]=None,
):
    if id:
        item=data.get(id)
    else:
        id, item=choice(list(data.items()))
    return {"id":id, "name": item}

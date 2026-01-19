from enum import Enum
from typing import Annotated
from pydantic import BaseModel, AfterValidator
from fastapi import FastAPI
from datetime import datetime
from db_conn import MySQL
from event_db import EventLog


class ModelName(str, Enum):
    alexnet="alexnext"
    resnet="resnet"
    lenet="lenet"

def check_user_id(id:int):
    if id not in MySQL().all_users("usuario"):
        raise ValueError("Erro ID de usuario invalido")
    return id

class Product(BaseModel):
    produto:str=None
    quantidade:int=None
    valor:float=None
    peso:float=None

class User(BaseModel):
    username:str
    email:str
    create_at:str=datetime.today().strftime("%d/%m/%Y")

app=FastAPI()

@app.get("/", include_in_schema=False) # -> False define não visivel a rota
async def root():
    return {"message":"Hello World"}

@app.get("/products/") # Read all products
async def read_products(
):
    return MySQL().all_products()

@app.get("/product/{id_product}") # Read a product
async def read_product(
    id:int
):
    return MySQL().read_product(id)

@app.post("/product/create/{owner_id}") # Create a product
async def create_product(
    owner_id:Annotated[int|None, AfterValidator(check_user_id)],product:Product
):
    product_dict=product.model_dump()
    msg=MySQL().create_product(
        user_id=owner_id, produto=product_dict["produto"], 
        quantidade=product_dict["quantidade"],
        valor=product_dict["valor"], peso=product_dict["peso"]
    )
    EventLog().create_event(msg, "outbox")

    return msg

@app.put("/product/edit/{id_product}/{owner_id}") # Edit a product
async def edit_product(
    id:int,owner_id:Annotated[int|None, AfterValidator(check_user_id)],product:Product
):
    if MySQL().read_product(id)["user_id"]==owner_id:
        print("User owner")
        product_dict=product.model_dump()
        if all(
            v!=None for v in product_dict.values()
        ):
            msg=MySQL().edit_product(owner_id, product_dict["produto"], product_dict["quantidade"], product_dict["valor"], product_dict["peso"])
            EventLog().create_event(msg, "outbox")
            return msg
    
    else :
        return "User not owner" 

@app.delete("/product/delete/{id_product}/{owner_id}") # Delete a product
async def delete_product(
    id:int,owner_id:Annotated[int|None, AfterValidator(check_user_id)]
):
    if MySQL().read_product(id)["user_id"]==owner_id:
        print("User owner")
        msg=MySQL().delete_product(id)
        
        EventLog().create_event(msg, "outbox")
        return 
    else :
        print("User not owner")
        return 


@app.post("/users/create/") # Create user
async def create_user(
    user:User
):
    user_dict=user.model_dump()
    msg=MySQL().create_user(username=user_dict["username"],email=user_dict["email"])
    print(f"{msg=}")
    EventLog().create_event(msg, "outbox")
    return user_dict

@app.get("/user/{id}") # Read a user
async def read_user(
    id:int
):
    user=MySQL().read_user(id)
    return user

@app.put("/users/{id}/") # Edit user
async def edit_user(
    id:int, user:User 
): 
    user_dict=user.model_dump()
    if user_dict['username']!=None and user_dict["email"]!=None and user_dict['username']!="string" and user_dict["email"]!="string":
        msg=MySQL().edit_user(user_dict["username"], user_dict["email"], id)
    elif user_dict['username']!=None or user_dict["email"]!=None:
        if user_dict['username']!=None and user_dict["email"]=="string" or user_dict["email"]==None:
            msg=MySQL().edit_user(user_dict["username"], None, id)

        if user_dict['email']!=None and user_dict["username"]=="string" or user_dict["username"]==None:
            msg=MySQL().edit_user(None, user_dict["email"], id)
    EventLog().create_event(msg, "outbox")
    return 

@app.delete("/del/user/{id}") # Delete user
async def delete_user(
    id:int,
):
    msg=MySQL().delete_user(id)
    EventLog().create_event(msg, "outbox")
    
    return 



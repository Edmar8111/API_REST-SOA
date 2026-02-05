from enum import Enum
from typing import Annotated
from pydantic import BaseModel, AfterValidator
from fastapi import FastAPI, Query
from datetime import datetime
from db_conn import MySQL
from event_db import EventLog
from product_service import ProductService
from user_service import UserService, UserDBManager
 

product_service=ProductService()
user_service=UserService()
# user_v2_service=UserDBManager()

def check_user_id(id:int):
    if id not in user_service.get_all_users():
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
    return product_service.get_all_products()

@app.get("/product/{id_product}") # Read a product
async def read_product(
    id:int
):
    product=product_service.read_product(id)
    return product

@app.post("/product/create/{owner_id}") # Create a product
async def create_product(
    owner_id:Annotated[int|None, 
    AfterValidator(check_user_id)],product:Product
):
    msg=product_service.create_product(product_dict=product.model_dump(), owner_id=owner_id)
    
    return msg

@app.put("/product/edit/{id_product}/{owner_id}") # Edit a product
async def edit_product(
    id:int,owner_id:Annotated[int|None, 
    AfterValidator(check_user_id)],product:Product
):
    if product_service.read_product(id)["user_id"]==owner_id:
        print("User owner")
        product_dict=product.model_dump()
        if all(v!=None for v in product_dict.values()):
            msg=product_service.edit_product(id, product_dict["produto"], product_dict["quantidade"], product_dict["valor"], product_dict["peso"])
            return msg
    else :
        return "User not owner" 

@app.delete("/product/delete/{id_product}/{owner_id}") # Delete a product
async def delete_product(
    id:int,owner_id:Annotated[int|None, AfterValidator(check_user_id)]
):
    if product_service.read_product(id)["user_id"]==owner_id:
        print("User owner")
        msg=product_service.delete_product(id)
        return msg
    else :
        print("User not owner")
        return 

# v1
@app.post("/users/v1/create/") # Create user
async def create_user(
    user:User
):
    user_dict=user.model_dump()
    msg=user_service.create_user(username=user_dict["username"],email=user_dict["email"])
    print(f"{msg=}")
    return msg

# v2
# @app.post("/users/v2/create") # Create User
# async def create_user_v2(
#     user:User
# ):
#     user_dict=user.model_dump()
#     msg=user_v2_service.create_user(**user_dict)
#     print(f"{msg=}")
#     return msg


@app.get("/user/{id}") # Read a user
async def read_user(
    id:int
):
    user=user_service.read_user(id)
    return user

@app.put("/users/{id}/") # Edit user
async def edit_user(
    id:int, user:User 
): 
    user_dict=user.model_dump()
    msg=user_service.edit_user(id, user_dict["username"], user_dict["email"])

    return msg

@app.delete("/del/user/{id}") # Delete user
async def delete_user(
    id:int,
):
    msg=user_service.delete_user(id)
    
    return msg




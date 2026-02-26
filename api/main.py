from enum import Enum
from typing import Annotated
from pydantic import BaseModel, AfterValidator
from fastapi import FastAPI, Query
from datetime import datetime
from db_conn import MySQL
from event_db import EventLog
from product_service import ProductService, ProductDBManager
from user_service import (UserService, UserDBManager,ServiceCreateV2, ServiceReadV2)
from decimal import Decimal

product_service = ProductService()
user_service = UserService()
user_v2_service = UserDBManager()
product_v2_service = ProductDBManager()


def check_user_id(id: int):
    if id not in user_service.get_all_users():
        raise ValueError("Erro ID de usuario invalido")
    return id


def check_user_id_v2(id: int):
    if id not in [i["id"] for i in user_v2_service.get_all_users()]:
        raise ValueError("Error ID de usuario invalido!")
    return id


class Product(BaseModel):
    produto: str = None
    quantidade: int = None
    valor: float = None
    peso: float = None


class User(BaseModel):
    username: str
    email: str
    create_at: str = datetime.today().strftime("%d/%m/%Y")


app = FastAPI()


@app.get("/", include_in_schema=False)  # -> False define não visivel a rota
async def root():
    return {"data": "API connection stabilished"}, 200

# v1
@app.get("/read-all/products/v1/")  # Read all products
async def read_products():
    return product_service.get_all_products(), 200

# v2
@app.get("/read-all/products/v2/")  # Read all products
async def read_products():
    return product_v2_service.read_all_products(), 200

# v1
@app.get("/read/product/v1/{id_product}")  # Read a product
async def read_product(id: int):
    product = product_service.read_product(id)
    return product, 200

# v2
@app.get("/read/product/v2/{id_product}")  # Read a product
async def read_product(id: int):
    product = product_v2_service.read_product(id)
    return product, 200

# v1 create product
@app.post("/create/product/v1/{owner_id}")  # Create a product
async def create_product_v1(
    owner_id: Annotated[int | None, AfterValidator(check_user_id)], product: Product
):
    msg = product_service.create_product(
        product_dict=product.model_dump(), owner_id=owner_id
    )

    return msg, 201

# v2 create product
@app.post("/create/product/v2/{owner_id}")  # Create a product v2
async def create_product_v2(
    owner_id: Annotated[int | None, AfterValidator(check_user_id_v2)], product: Product
):
    product_dict = product.model_dump()
    produto, quantidade, valor, peso=(
        str(product_dict["produto"]), int(product_dict["quantidade"]),
        Decimal(product_dict["valor"]), Decimal(product_dict["peso"]
    ))
    print(f"{product_dict}")

    msg=product_v2_service.create_product(
        user_id=owner_id, produto=produto, quantidade=quantidade,
        valor=valor, peso=peso)
    return msg, 202

# v1
@app.put("/update/product/v1/{id_product}/{owner_id}")  # Edit a product
async def edit_product(
    id: int,
    owner_id: Annotated[int | None, AfterValidator(check_user_id)],
    product: Product,
):
    if product_service.read_product(id)["user_id"] == owner_id:
        print("User owner")
        product_dict = product.model_dump()
        if all(v != None for v in product_dict.values()):
            msg = product_service.edit_product(
                id,
                product_dict["produto"],
                product_dict["quantidade"],
                product_dict["valor"],
                product_dict["peso"],
            )
            return msg
    else:
        return "User not owner"


# v1
@app.delete("/del/product/v1/{id_product}/{owner_id}")  # Delete a product
async def delete_product(
    id: int, owner_id: Annotated[int | None, AfterValidator(check_user_id)]
):
    if product_service.read_product(id)["user_id"] == owner_id:
        print("User owner")
        msg = product_service.delete_product(id)
        return msg, 204
    else:
        print("User not owner")
        return

# v2
@app.delete("/product/v2/delete/{id_product}/{owner_id}")  # Delete a product
async def delete_product(
    id: int, owner_id: Annotated[int | None, AfterValidator(check_user_id_v2)]
):
    if product_v2_service.read_product(id)["user_id"] == owner_id:
        print("User owner")
        msg = product_v2_service.delete_product(id)
        return msg, 204
    else:
        print("User not owner")
        return


# v1
@app.post("/create/users/v1/")  # Create user
async def create_user_v1(user: User):
    user_dict = user.model_dump()
    msg = user_service.create_user(
        username=user_dict["username"], email=user_dict["email"]
    )
    print(f"{msg=}")
    return msg, 202


# v2
@app.post("/create/users/v2")  # Create User
async def create_user_v2(user: User):
    user_dict = user.model_dump()
    msg = user_v2_service.create_user(**user_dict)
    print(f"{msg=}")
    return msg, 202

# versão via super()
@app.post("/create/users/v3")
async def create_user_v3(user:User):
    user_dict = user.model_dump()
    create_user = ServiceCreateV2(**user_dict).create_user
    return f"Usuario {user_dict['username']} criado!"

#v1
@app.get("/read/user/v1/{id}")  # Read a user 
async def read_user(id: int):
    user = user_service.read_user(id)
    return user, 200

# v2
@app.get("/read/user/v2/{id}")  # Read a user
async def read_user(id: int):
    user = user_v2_service.get_user_by_id(id)
    return user, 200


# versão via super()
@app.get("/read/user/v3/{id}")
async def read_user(id:int|None=None):
    user=ServiceReadV2(id).get_user_by_id
    return f"{user}"

# v1
@app.put("/update/user/v1/{id}/")  # Update user
async def edit_user(id: int, user: User):
    user_dict = user.model_dump()
    msg = user_service.edit_user(id, user_dict["username"], user_dict["email"])

    return msg, 202

#v2
@app.put("/update/user/v2/{id}/")  # Update user
async def edit_user(id: int, user: User):
    user_dict = user.model_dump()
    msg = user_v2_service.update_user(id=id, username=user_dict["username"], email=user_dict["email"])

    return msg, 202


# v1
@app.delete("/del/user/v1/{id}")  # Delete user
async def delete_user(
    id: int,
):
    msg = user_service.delete_user(id)

    return msg, 204

# v2
@app.delete("/del/user/v2/{id}")  # Delete user
async def delete_user(
    id: int,
):
    msg = user_v2_service.delete_user(id)

    return msg, 204


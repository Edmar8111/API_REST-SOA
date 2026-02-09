from enum import Enum
from typing import Annotated
from pydantic import BaseModel, AfterValidator
from fastapi import FastAPI, Query
from datetime import datetime
from db_conn import MySQL
from event_db import EventLog
from product_service import ProductService, ProductDBManager
from user_service import UserService, UserDBManager
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


@app.get("/products/")  # Read all products
async def read_products():
    return product_service.get_all_products(), 200


@app.get("/product/{id_product}")  # Read a product
async def read_product(id: int):
    product = product_service.read_product(id)
    return product, 200


# v1 create product
@app.post("/product/v1/create/{owner_id}")  # Create a product
async def create_product_v1(
    owner_id: Annotated[int | None, AfterValidator(check_user_id)], product: Product
):
    msg = product_service.create_product(
        product_dict=product.model_dump(), owner_id=owner_id
    )

    return msg, 201


# v2 create product
@app.post("/product/v2/create/{owner_id}")  # Create a product v2
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
    return msg, 201

@app.put("/product/edit/{id_product}/{owner_id}")  # Edit a product
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


@app.delete("/product/delete/{id_product}/{owner_id}")  # Delete a product
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


# v1
@app.post("/users/v1/create/")  # Create user
async def create_user_v1(user: User):
    user_dict = user.model_dump()
    msg = user_service.create_user(
        username=user_dict["username"], email=user_dict["email"]
    )
    print(f"{msg=}")
    return msg, 201


# v2
@app.post("/users/v2/create")  # Create User
async def create_user_v2(user: User):
    user_dict = user.model_dump()
    msg = user_v2_service.create_user(**user_dict)
    print(f"{msg=}")
    return msg, 201


@app.get("/user/{id}")  # Read a user
async def read_user(id: int):
    user = user_service.read_user(id)
    return user, 200


@app.put("/users/{id}/")  # Edit user
async def edit_user(id: int, user: User):
    user_dict = user.model_dump()
    msg = user_service.edit_user(id, user_dict["username"], user_dict["email"])

    return msg


@app.delete("/del/user/{id}")  # Delete user
async def delete_user(
    id: int,
):
    msg = user_service.delete_user(id)

    return msg, 204

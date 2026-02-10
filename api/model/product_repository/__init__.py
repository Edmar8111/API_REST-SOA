from .. import create, read, update, delete 
from typing import Optional, Dict

create=create.CreateModel(),    

def ReadAll():
    return read.ReadModel().get_all_products()

def ReadById(id: Optional[int|None]):
    return read.ReadModel(id).get_product_by_id()

def CreateProduct(**product_data):
    return create.create_product(**product_data)

def DeleteProduct(id:Optional[int|None]):
    return delete.DeleteModel(id).delete_product()
from .. import read, create

create=create.CreateModel()

def ReadAll():
    return read.get_all_products()


def ReadById(product_id: int):
    return read.get_product_by_id(product_id)


def CreateProduct(**product_data):
    return create.create_product(**product_data)

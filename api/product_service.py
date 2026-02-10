from model import product_repository
from product_repository import ProductRepository
from event_db import EventLog
from typing import Optional, Dict

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
        self.eventLog = EventLog()

    def get_all_products(self):
        return self.repository.all_products()

    def create_product(self, **kwargs):
        msg = self.repository.create_product(
            user_id=kwargs["owner_id"],
            produto=kwargs["product_dict"]["produto"],
            quantidade=kwargs["product_dict"]["quantidade"],
            valor=kwargs["product_dict"]["valor"],
            peso=kwargs["product_dict"]["peso"],
        )
        self.eventLog.create_event(msg, "outbox")

        return "Produto criado com sucesso!"

    def delete_product(self, id):
        msg = self.repository.delete_product(id)
        self.eventLog.create_event(msg, "outbox")

        return "Produto deletado com sucesso!"

    def read_product(self, id):
        return self.repository.read_product(id)

    def edit_product(self, *args):
        msg = self.repository.edit_product(*args)
        self.eventLog.create_event(msg, "outbox")

        return "Produto atualizado com sucesso!"


class ProductDBManager:
    """Classe para gerenciar conexões e operações com o banco de dados MySQL."""

    def __init__(self):
        pass

    def create_product(product_data:Optional[Dict|None]):
        return product_repository.CreateProduct(
                user_id=product_data['user_id'], 
                produto=product_data['produto'],
                quantidade=product_data['quantidade'],
                valor=product_data['valor'],
                peso=product_data['peso']
               )

    def read_all_products(self):
        return product_repository.ReadAll()
    
    def read_product(id:Optional[int|None]):
        return product_repository.ReadById(id=id)
    
    def update_product(self):
        pass
        
    def delete_product(self, id:Optional[int|None]):
        return product_repository.DeleteProduct(id)
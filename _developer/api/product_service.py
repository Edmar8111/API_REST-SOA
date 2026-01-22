from product_repository import ProductRepository
from event_db import EventLog 


class ProductService:
    def __init__(self):
        self.repository=ProductRepository()
        self.eventLog=EventLog()
        
    def get_all_products(self):
        return self.repository.all_products()

    def create_product(self, **kwargs):
        msg=self.repository.create_product(
            user_id=kwargs["owner_id"], produto=kwargs["product_dict"]["produto"], 
            quantidade=kwargs["product_dict"]["quantidade"],
            valor=kwargs["product_dict"]["valor"], peso=kwargs["product_dict"]["peso"]
        )
        self.eventLog.create_event(msg, "outbox")

        return "Produto criado com sucesso!"

    def delete_product(self, id):
        msg=self.repository.delete_product(id)
        self.eventLog.create_event(msg, "outbox")

        return "Produto deletado com sucesso!"
     
    def read_product(self, id):
        return self.repository.read_product(id)
    
    def edit_product(self, *args):
        msg=self.repository.edit_product(*args)
        self.eventLog.create_event(msg, "outbox")

        return "Produto atualizado com sucesso!"
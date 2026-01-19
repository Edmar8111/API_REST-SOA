import produto_repository
import event_db 


class ProductService:
    def __init__(self, repository=produto_repository):
        self.repository=repository
        self.eventlog=event_db.EventLog()
        pass
    def get_all_products(self):
        return self.repository.all_products()

    def create_product(self, product_dict, owner_id):
        msg=self.repository.create_product(
            user_id=owner_id, produto=product_dict["produto"], 
            quantidade=product_dict["quantidade"],
            valor=product_dict["valor"], peso=product_dict["peso"]
        )
        self.eventlog.create_event(msg, "outbox")

        return msg

    def delete_product(self, id):

        return self.repository.delete_product(id)
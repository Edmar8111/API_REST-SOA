import produto_repository
import event_db 


class ProductService:
    def __init__(self):
        self.repository=produto_repository
        self.eventlog=event_db.EventLog()
        pass
    def get_all_products(self):
        return self.repository.all_products()

    def create_product(self, **kwargs):
        msg=self.repository.create_product(
            user_id=kwargs["owner_id"], produto=kwargs["product_dict"]["produto"], 
            quantidade=kwargs["product_dict"]["quantidade"],
            valor=kwargs["product_dict"]["valor"], peso=kwargs["product_dict"]["peso"]
        )
        self.eventlog.create_event(msg, "outbox")

        return msg

    def delete_product(self, id):


        return self.repository.delete_product(id)

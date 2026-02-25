from model import user_repository
from user_repository import UserRepository
from event_db import EventLog
from typing import Optional, Dict

class UserService:
    def __init__(self):
        self.repository=UserRepository()
        self.eventLog=EventLog()
        pass

    def get_all_users(self):
        return self.repository.all_users()
    
    def read_user(self, id):
        return self.repository.read_user(id)
    
    def create_user(self, **kwargs):
        msg=self.repository.create_user(**kwargs)
        self.eventLog.create_event(msg, "outbox")

        return "Usuario criado com sucesso!"

    def delete_user(self, id):
        msg=self.repository.delete_user(id)
        self.eventLog.create_event(msg, "outbox")

        return "Usuario Deletado com sucesso!" 

    def edit_user(self, *args):
        msg=self.repository.edit_user(*args)
        self.eventLog.create_event(msg, "outbox")
        
        return msg
    
class UserDBManager:
    def __init__(self):
        pass
    
    def get_all_users(self):
        return user_repository.ReadAll()
    
    def get_user_by_id(self, user_id: int):
        return user_repository.ReadById(user_id)
    
    def create_user(self, user_data:Optional[Dict|None]):
        return user_repository.CreateUser(username=user_data['username'], email=user_data['email'])
    
    def update_user(self, update_data:Optional[Dict|None]):
        return user_repository.UpdateUser(id=update_data['id'], username=update_data['username'], email=update_data['email']) 



from api.model.crud import Read


class ServiceReadV2(Read):
    def __init__(self, id:int|None=None):
        super().__init__(id)

    def get_all_user(self):
        return super().get_all_user()
    
    def get_user_by_id(self):
        return super().get_user_by_id()
    
    def get_all_products(self):
        return super().get_all_products()
    
    def get_product_by_id(self):
        return super().get_product_by_id()
    
from model import user_repository
from user_repository import UserRepository
from event_db import EventLog

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
    
    def create_user(self, **user_data):
        return user_repository.CreateUser(**user_data)
    
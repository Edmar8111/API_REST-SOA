from .dataBaseManager import Database

from abc import ABC, abstractmethod

class Create(ABC):
    def __init__(self, **data):
        self.db=Database()
        self.data=data
        
    @abstractmethod
    def create_user(self):
        try:
            query = "INSERT INTO usuario (username, email) VALUE (%s, %s)"
            self.db.execute(query, (self.data['name'], self.data['email']))
            self.db.commit()
        finally:
            pass


class Read(ABC):
    
    def __init__(self, id:int|None=None):
        print("REQUESTE")
        self.db=Database()
        self.id=id
     
    @abstractmethod   
    def get_all_user(self):
        try:
            query="SELECT id, username, email FROM usuario"
            return self.db.fetch_all(query)
        finally:
            pass
    
    @abstractmethod
    def get_user_by_id(self):
        try:
            query="SELECT id, username, email FROM usuario WHERE id = %s"
            return self.db.fetch_one(query, (self.id))
        finally:
            pass
    
    @abstractmethod
    def get_all_products(self):
        try:
            query = "SELECT user_id, produto, quantidade, valor, peso FROM produto"
            return self.db.fetch_all(query)
        finally:
            pass
    
    @abstractmethod
    def get_product_by_id(self):
        try:
            query = "SELECT user_id, produto, quantidade, valor, peso FROM produto WHERE id = %s"
            return self.db.fetch_one(query, (self.id,))
        finally:
            pass
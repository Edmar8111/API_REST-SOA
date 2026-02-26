from .dataBaseManager import Database

from abc import ABC, abstractmethod

class Create(ABC):
    def __init__(self, **data):
        self.db=Database()
        self.data=data
        print(f"{data=}")
        
    @abstractmethod
    def create_user(self):
        try:
            query = "INSERT INTO usuario (username, email) VALUE (%s, %s)"
            self.db.execute(query, (self.data['name'], self.data['email']))
            self.db.commit()
        finally:
            pass
    
    @abstractmethod
    def create_product(self):
        try:
            query = "INSERT INTO (user_id, produto, quantidade, valor, peso) VALUES (%s, %s, %s, %s, %s)"
            self.db.execute(query, (self.data['user_id'], self.data['produto'], self.data['quantidade'], self.data['valor'], self.data['peso']))
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
        
class Update(ABC):
    pass

class Delete(ABC):
    def __init__(self, id:int|None=None):
        self.db=Database()
        self.id=id
    
    @abstractmethod
    def delete_user(self):
        try:
            query = "DELETE FROM usuario WHERE id = %s"
            self.db.execute(query, (self.id,))
        finally:
            pass
    
    @abstractmethod
    def delete_product(self):
        try:
            query = "DELETE FROM produto WHERE id = %s"
            self.db.execute(query, (self.id,))
        finally:
            pass
        
        
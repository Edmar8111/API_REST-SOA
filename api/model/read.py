from typing import Optional

"""Módulo responsável pelas operações de leitura no banco de dados."""

from .dataBaseManager import Database

class ReadModel:
    def __init__(self, id=Optional[int|None]):
        """_summary_
        :param id: ID único do usuário.
        """
        self.db=Database()
        self.id=id
        
    def get_all_users(self):
        """
        Recupera todos os usuários cadastrados.

        :return: Lista de tuplas com os dados dos usuários.
        """
        try:
            query = "SELECT id, username, email FROM usuario"
            return self.db.fetch_all(query)
        finally:
            pass
            # db.close()

    def get_user_by_id(self):
        """
        Busca um usuário específico pelo ID.
        
        :return: Tupla com dados do usuário ou None.
        """
        try:
            query = "SELECT id, username, email FROM usuario WHERE id = %s"
            return self.db.fetch_one(query, (self.id,))
        finally:
            pass
            # db.close()

    def get_all_products(self):
        """
        Recupera todos os produtos cadastrados.
        
        :return: Lista de tuplas com os dados dos produtos.
        """
        try:
            query = "SELECT user_id, produto, quantidade, valor, peso FROM produto"
            return self.db.fetch_all(query)
        finally:
            pass
            # db.close() 
    
    def get_product_by_id(self):
        """
        Busca um produto específico pelo ID.
        
        :return: Tupla com dados do produto ou None.
        """
        db = Database()
        try:
            query = "SELECT user_id, produto, quantidade, valor, peso FROM produto WHERE id = %s"
            return self.db.fetch_one(query, (self.id,))
        finally:
            pass
            # db.close()



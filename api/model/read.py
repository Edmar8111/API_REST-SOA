"""Módulo responsável pelas operações de leitura no banco de dados."""

from .dataBaseManager import Database

class ReadModel:
    def __init__(self):
        self.db=Database()
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

    def get_user_by_id(self,user_id: int):
        """
        Busca um usuário específico pelo ID.

        :param user_id: ID único do usuário.
        :return: Tupla com dados do usuário ou None.
        """
        db = Database()
        try:
            query = "SELECT id, username, email FROM usuario WHERE id = %s"
            return self.db.fetch_one(query, (user_id,))
        finally:
            pass
            # db.close()


"""Módulo responsável pelas operações de exclusão no banco de dados."""

from .dataBaseManager import Database

class DeleteModel:
    def __init__(self, id):
        """
        Docstring for __DeleteModel__
        
        :param id: ID do usuário a ser removido.
        """
        
        self.db=Database()
        self.id=id
    
    def delete_user(self) -> None:
        """
        Remove um usuário do banco de dados pelo ID.

        """
        try:
            query = "DELETE FROM usuario WHERE id = %s"
            self.db.execute(query, (self.id,))
            print(f"Usuário {self.id} removido com sucesso.")
        except Exception as e:
            print(f"Erro ao deletar: {e}")
        finally:
            pass
        
    def delete_product(self) -> None:
        """
        Remove um produto do banco de dados pelo ID.
        """
        try:
            query = "DELETE FROM produto WHERE id = %s"
            self.db.execute(query, (self.id,))
            print(f"Usuário {self.id} removido com sucesso.")
        except Exception as e:
            print(f"Erro ao deletar: {e}")
        finally:
            pass
            # db.close()


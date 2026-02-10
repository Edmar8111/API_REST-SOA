"""Módulo responsável pelas operações de atualização no banco de dados."""

from .dataBaseManager import Database

class UpdateUserModel:
    def __init__(
        self,
        **update_data
    ) -> None:
        self.db=Database()
        self.id=update_data["id"]
        self.new_username=update_data["username"]
        self.new_email=update_data['email']

    def update_user_email(
        self,
    ) -> None:
        """
        Atualiza o username de um usuário existente.

        :param user_id: ID do usuário a ser atualizado.
        :param new_username: Aloca dados atualizados.
        """
        try:
            if self.new_username!=None:
                query = "UPDATE usuario SET username = %s WHERE id = %s"
                self.db.execute(query, (self.new_username, self.id))
                print(f"Username alterdo para -> {self.new_username}. usuário {self.id} atualizado com sucesso.")
        except Exception:
            print(f"{Exception=}")
        finally:
            pass
        
    def update_user_email(
        self,
    ) -> None:
        """
        Atualiza o email de um usuário existente.

        :param user_id: ID do usuário a ser atualizado.
        :param new_email: Aloca dados atualizados.
        """
        try:
            if self.new_email!=None:
                query = "UPDATE usuario SET email = %s WHERE id = %s"
                self.db.execute(query, (self.new_email, self.id))
                print(f"Email alterado para -> {self.new_email} do usuário {self.id} atualizado com sucesso.")
        except Exception:
            print(f"{Exception=}")
        finally:
            pass
            # db.close()

class UpdateProductModel:
    pass

"""Módulo responsável pelas operações de criação no banco de dados."""

from .dataBaseManager import Database


class CreateModel:
    def __init__(self):
        self.db = Database()

    def create_user(self, **user_data) -> None:
        print(f"CONEXÃO DO BANCO -> {self.db=}")
        name, email = (user_data["username"], user_data["email"])
        """
        Insere um novo usuário na tabela 'users'.

        :param name: Nome do usuário a ser inserido.
        :param email: Email do usuário a ser inserido.
        """
        try:
            query = "INSERT INTO usuario (username, email) VALUES (%s, %s)"
            self.db.execute(query, (name, email))
            print(f"Usuário {name} criado com sucesso.")
            self.db.commit()

        except Exception as e:
            print(f"Database error connection -> {e}")
        finally:
            # self.db.close()
            pass

    def create_product(self, **product_data):
        user_id, produto, quantidade, valor, peso = (
            product_data["user_id"],
            product_data["produto"],
            product_data["quantidade"],
            product_data["valor"],
            product_data["peso"],
        )
        try:
            yield self.db
            query = "INSERT INTO produto (user_id, produto, quantidade, valor, peso) VALUES (%s, %s, %s, %s, %s)"
            self.db.execute(query, (user_id, produto, quantidade, valor, peso))
            print(f"Produto criado -> {produto}")
        except Exception as e:
            print(f"Database error connection -> {e}")
     
        finally:
            # self.db.close()
            pass

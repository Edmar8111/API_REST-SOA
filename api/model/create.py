"""Módulo responsável pelas operações de criação no banco de dados."""

from .dataBaseManager import Database


def create_user(**user_data) -> None:
    name,email=(user_data["username"], user_data["email"])
    """
    Insere um novo usuário na tabela 'users'.

    :param name: Nome do usuário a ser inserido.
    :param email: Email do usuário a ser inserido.
    """
    db = Database()
    try:
        query = "INSERT INTO usuario (username, email) VALUES (%s, %s)"
        db.execute(query, (name, email))
        print(f"Usuário {name} criado com sucesso.")
    finally:
        db.close()

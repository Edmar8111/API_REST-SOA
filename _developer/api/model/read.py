"""Módulo responsável pelas operações de leitura no banco de dados."""

from dataBaseManager import Database

def get_all_users():
    """
    Recupera todos os usuários cadastrados.

    :return: Lista de tuplas com os dados dos usuários.
    """
    db = Database()
    try:
        query = "SELECT id, name, email FROM users"
        return db.fetch_all(query)
    finally:
        db.close()

def get_user_by_id(user_id: int):
    """
    Busca um usuário específico pelo ID.

    :param user_id: ID único do usuário.
    :return: Tupla com dados do usuário ou None.
    """
    db = Database()
    try:
        query = "SELECT id, name, email FROM users WHERE id = %s"
        return db.fetch_one(query, (user_id,))
    finally:
        db.close()

if __name__ == "__main__":
    users = get_all_users()
    for user in users:
        print(user)
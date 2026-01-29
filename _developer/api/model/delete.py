"""Módulo responsável pelas operações de exclusão no banco de dados."""

from dataBaseManager import Database

def delete_user(user_id: int) -> None:
    """
    Remove um usuário do banco de dados pelo ID.

    :param user_id: ID do usuário a ser removido.
    """
    db = Database()
    try:
        query = "DELETE FROM users WHERE id = %s"
        db.execute(query, (user_id,))
        print(f"Usuário {user_id} removido com sucesso.")
    except Exception as e:
        print(f"Erro ao deletar: {e}")
    finally:
        db.close()


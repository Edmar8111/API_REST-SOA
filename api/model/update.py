"""Módulo responsável pelas operações de atualização no banco de dados."""

from .dataBaseManager import Database

def update_user_email(user_id: int, new_email: str) -> None:
    """
    Atualiza o email de um usuário existente.

    :param user_id: ID do usuário a ser atualizado.
    :param new_email: Novo endereço de email.
    """
    db = Database()
    try:
        query = "UPDATE users SET email = %s WHERE id = %s"
        db.execute(query, (new_email, user_id))
        print(f"Email do usuário {user_id} atualizado com sucesso.")
    finally:
        db.close()

if __name__ == "__main__":
    update_user_email(1, "novo_email@email.com")
"""
Módulo de leitura do CRUD.

Permite a busca de todos os usuários ou de um usuário específico
através da passagem de argumentos via linha de comando.
"""

import argparse
import sys
from dataBaseManager import Database

def get_all_users():
    """
    Recupera todos os usuários cadastrados.

    :return: Lista de registros encontrados.
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

    :param user_id: ID numérico do usuário.
    :return: Registro encontrado ou None.
    """
    db = Database()
    try:
        query = "SELECT id, name, email FROM users WHERE id = %s"
        return db.fetch_one(query, (user_id,))
    finally:
        db.close()

def main():
    """
    Configura e gerencia a interface de linha de comando (CLI).
    """
    parser = argparse.ArgumentParser(description="Utilitário de Leitura de Usuários")
    
    # Define o argumento opcional --id. Se não passado, o padrão é None.
    parser.add_argument(
        "--id", 
        type=int, 
        help="ID do usuário para busca específica"
    )

    args = parser.parse_args()

    if args.id:
        user = get_user_by_id(args.id)
        if user:
            print(f"Usuário encontrado: {user}")
        else:
            print(f"Nenhum usuário encontrado com o ID {args.id}.")
    else:
        users = get_all_users()
        print(f"--- Lista de Usuários ({len(users)}) ---")
        for u in users:
            print(u)

if __name__ == "__main__":
    main()
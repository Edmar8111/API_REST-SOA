"""Módulo responsável por executar a criação das tabelas no banco de dados."""

import sys
from ..dataBaseManager import Database
from schema import get_setup_script

def initialize_tables() -> None:
    """
    Instancia a conexão e executa o script de estruturação das tabelas.
    """
    db = Database()
    print("Conectado ao banco. Iniciando criação das tabelas...")
    
    try:
        sql_script = get_setup_script()
        
        # Como o MySQLdb não possui o método 'executescript' do SQLite, 
        # precisamos dividir as queries ou executá-las individualmente.
        # Aqui, filtramos linhas vazias e comentários para execução limpa.
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
        
        for command in commands:
            db.execute(command)
            
        print("Estrutura do banco de dados criada/validada com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}", file=sys.stderr)
    finally:
        db.close()

if __name__ == "__main__":
    # Permite execução via shell: python setup_db.py
    initialize_tables()
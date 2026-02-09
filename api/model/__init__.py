from . import create, read, update, delete
from .schema import setup_db

print("INICIALIZADO A ESTRUTURAÇÃO DAS TABELAS...")

setup_db.initialize_tables()

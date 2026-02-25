from . import create, read, update, delete

#========================= debug =====================
# Tabelas
try:
    from .schema import setup_db
    setup_db.initialize_tables()
except:
    raise Exception
#======================================================
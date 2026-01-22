import sqlite3
import os

DATABASE=os.path.abspath("database.db")

class MySQL:
    
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE, timeout=3)
        print("Conexão estabelecida.")
        self.cursor=self.conn.cursor()
        
        # Retorna linhas como dict-like (acesso por nome de coluna)
        self.conn.row_factory=sqlite3.Row

        # IMPORTANTE: SQLite só aplica FK se isso estiver ativo
        self.conn.execute("PRAGMA foreign_keys = ON;")

        self.cursor.execute("PRAGMA journal_mode=WAL;")
        self.cursor.execute("PRAGMA synchronous=NORMAL;")
        self._criar_tabelas()
    
    def _close(self):
        return self.conn.close()
    
    def _criar_tabelas(self):

        self.conn.executescript("""

            -- =========================
            -- TABELA: usuario
            -- =========================          
            CREATE TABLE IF NOT EXISTS usuario (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE,
                email         TEXT    NOT NULL UNIQUE,
                data_criacao  TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            -- =========================
            -- TABELA: produtos
            -- =========================
            CREATE TABLE IF NOT EXISTS produtos (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                produto    TEXT    NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
                valor      REAL    NOT NULL DEFAULT 0 CHECK (valor >= 0),
                peso       REAL    NOT NULL DEFAULT 0 CHECK (peso >= 0),

                CONSTRAINT fk_produtos_usuario
                    FOREIGN KEY (user_id)
                    REFERENCES usuario(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_produtos_user_id ON produtos(user_id);
            
        """)
        self.conn.commit()
        
        return 
    
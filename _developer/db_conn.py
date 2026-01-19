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
    
    def all_users(self, table):
        try:
            selectAll=self.conn.execute(f'SELECT * FROM {table}').fetchall()
            users=[i['id'] for i in selectAll]
            return users

        except ValueError as e:
            raise f"Erro ao retornar dados {e}"
    
        finally:
            self._close()
    
    def read_user(self, id):
        try:
            row=self.conn.execute(f"SELECT * FROM usuario WHERE id=?",(id,)).fetchone()
            return dict(row) if row else None

        except ValueError as e:
            raise f"Erro ao ler usuario {e}"
        finally:
            self._close()
        
    def create_user(self, **kwargs):
        username,email=(kwargs["username"], kwargs["email"])
        try:
            self.conn.execute('INSERT INTO usuario (username, email) VALUES (?, ?)', (username, email))
            self.conn.commit()
            return f'Usuario {username} criado'
        except ValueError as e:
            raise f'Usuario não cadastrado {e}'
        finally:
            self._close()
    
    def edit_user(self,*args):
        username,email,id=args
        try:
            if username!=None and email!=None:
                #efetua a alteração de ambos os valores
                self.conn.execute("UPDATE usuario SET username=?, email=? WHERE id=?", (username, email, id))
                self.conn.commit()

            elif  username!=None or email!=None:
                if username!=None:
                    #Efetua a alteração do nome
                    self.conn.execute("UPDATE usuario SET username=? WHERE id=?", (username, id))
                    self.conn.commit()
                elif email!=None:
                    #Efetua a alteração do email
                    self.conn.execute("UPDATE usuario SET email=? WHERE id=?", (email,id))
                    self.conn.commit()
                
            return f'Usuario atualizado'
        
        except ValueError as e:
            raise f"Erro ao atualizar dados {e}"
        
        finally:
            self._close()

    def delete_user(self, id):
        try:
            self.conn.execute("DELETE FROM usuario WHERE id=?",(id,))
            self.conn.commit()
            return 'User Delete'
        except ValueError as e:
            raise f"Erro ao deletar usuario {e}"
        finally:
            self._close()

    def create_product(self,**kwargs):
        user_id,produto,quantidade,valor,peso=(
            kwargs["user_id"], kwargs["produto"],
            kwargs["quantidade"], kwargs["valor"],
            kwargs["peso"]
        )
        try:
            self.conn.execute('INSERT INTO produtos (user_id, produto, quantidade, valor, peso) VALUES (?, ?, ?, ?, ?)', 
                (user_id, produto, quantidade, valor, peso)
            )
            self.conn.commit()
            return f'Produto {produto} criado'
        except ValueError as e:
            raise f'Produto não cadastrado {e}'
        finally:
            self._close()

    def read_product(self, id):
        try:
            row=self.conn.execute(f"SELECT * FROM produtos WHERE id=?",(id,)).fetchone()
            return dict(row) if row else None

        except ValueError as e:
            raise f"Erro ao ler produto {e}"
        finally:
            self._close()

    def all_products(self):
        try:
            selectAll=self.conn.execute(f'SELECT * FROM produtos').fetchall()
            products=[i for i in selectAll]
            return products

        except ValueError as e:
            raise f"Erro ao retornar dados {e}"
    
        finally:
            self._close()
    
    def delete_product(id):
        try:
            self.conn.execute("DELETE FROM produtos WHERE id=?",(id,))
            self.conn.commit()
            return 'Produto Deletado'
        except ValueError as e:
            raise f"Erro ao deletar produto {e}"
        finally:
            self._close()

    def edit_product(self,*args):
        id,produto,quantidade,valor,peso=args
        
        try:
            if produto!=None and quantidade!=None and valor!=None and peso!=None:
                #efetua a alteração de ambos os valores
                self.conn.execute("UPDATE produtos SET produto=?, quantidade=?, valor=?, peso=? WHERE id=?", (produto, quantidade, valor, peso, id))
                self.conn.commit()

            elif  produto!=None or quantiade!=None or valor!=None or peso!=None:
                if produto!=None:
                    #Efetua a alteração do nome
                    self.conn.execute("UPDATE produtos SET produto=? WHERE id=?", (produto, id))
                    self.conn.commit()
                elif quantidade!=None:
                    #Efetua a alteração do email
                    self.conn.execute("UPDATE produtos SET quantidade=? WHERE id=?", (quantidade,id))
                    self.conn.commit()
                elif valor!=None:
                    #Efetua a alteração do email
                    self.conn.execute("UPDATE produtos SET valor=? WHERE id=?", (valor,id))
                    self.conn.commit()
                elif peso!=None:
                    #Efetua a alteração do email
                    self.conn.execute("UPDATE produtos SET peso=? WHERE id=?", (peso,id))
                    self.conn.commit()
                
            return f'Usuario atualizado'
        
        except ValueError as e:
            raise f"Erro ao atualizar dados {e}"
        
        finally:
            self._close()


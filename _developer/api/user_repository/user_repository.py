import db_conn
from datetime import datetime

class UserRepository:
    def __init__(self):
        self.db_client=db_conn.MySQL()
    
    def all_users(self):
        try:
            selectAll=self.db_client.conn.execute(f'SELECT * FROM usuario').fetchall()
            users=[i['id'] for i in selectAll]
            return users

        except ValueError as e:
            raise f"Erro ao retornar dados {e}"
    
        finally:
            self.db_client._close()
    
    def read_user(self, id):
        try:
            row=self.db_client.conn.execute(f"SELECT * FROM usuario WHERE id=?",(id,)).fetchone()
        except ValueError as e:
            raise f"Erro ao ler usuario {e}"
        finally:
            return dict(row) if row else None
            
    def create_user(self, **kwargs):
        username,email=(kwargs["username"], kwargs["email"])
        try:
            self.db_client.conn.execute('INSERT INTO usuario (username, email) VALUES (?, ?)', (username, email))
            self.db_client.conn.commit()
            return f'Usuario {username} criado {datetime.today().strftime("%d/%m/%Y")}'
        except ValueError as e:
            raise f'Usuario não cadastrado {e}'
        finally:
            self.db_client._close()
        
    def delete_user(self, id):
        try:
            username=self.read_user(id)['username'                                        ]
            self.db_client.conn.execute("DELETE FROM usuario WHERE id=?",(id,))
            self.db_client.conn.commit()
            return f'Usuario {username} Deletado {datetime.today().strftime("%d/%m/%Y")}'
        except ValueError as e:
            raise f"Erro ao deletar usuario {e}"
        finally:
            self.db_client._close()

    def edit_user(self,*args):
        id,username,email=args
        try:
            if username!=None and email!=None:
                #efetua a alteração de ambos os valores
                self.db_client.conn.execute("UPDATE usuario SET username=?, email=? WHERE id=?", (username, email, id))
                self.db_client.conn.commit()

            elif  username!=None or email!=None:
                if username!=None:
                    #Efetua a alteração do nome
                    self.db_client.conn.execute("UPDATE usuario SET username=? WHERE id=?", (username, id))
                    self.db_client.conn.commit()
                elif email!=None:
                    #Efetua a alteração do email
                    self.db_client.conn.execute("UPDATE usuario SET email=? WHERE id=?", (email,id))
                    self.db_client.conn.commit()
                
            return f'Usuario atualizado'
        
        except ValueError as e:
            raise f"Erro ao atualizar dados {e}"
        
        finally:
            self.db_client._close()
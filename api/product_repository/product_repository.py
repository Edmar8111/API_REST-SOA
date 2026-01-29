import db_conn
from datetime import datetime

class ProductRepository:
    def __init__(self):
        self.db_client=db_conn.MySQL()

    def all_products(self):
        try:
            self.selectAll=self.db_client.conn.execute(f'SELECT * FROM produtos').fetchall()
            self.products=[i for i in self.selectAll]
            return self.products

        except ValueError as e:
            raise f"Erro ao retornar dados {e}"
    
        finally:
            pass

    def delete_product(self, id):
        try:
            produto=self.read_product(id)['produto']
            self.db_client.conn.execute("DELETE FROM produtos WHERE id=?",(id,))
            self.db_client.conn.commit()
            return f'Produto {produto}:{id} Deletado {datetime.today().strftime("%d/%m/%Y")}'
        except ValueError as e:
            raise f"Erro ao deletar produto {e}"
        finally:
            pass

    def create_product(self,**kwargs):
        self.user_id,produto,quantidade,valor,peso=(
            kwargs["user_id"], kwargs["produto"],
            kwargs["quantidade"], kwargs["valor"],
            kwargs["peso"]
        )
        try:
            self.db_client.conn.execute('INSERT INTO produtos (user_id, produto, quantidade, valor, peso) VALUES (?, ?, ?, ?, ?)', 
                (self.user_id, produto, quantidade, valor, peso)
            )
            self.db_client.conn.commit()
            return f'Produto {produto} criado {datetime.today().strftime("%d/%m/%Y")}'
        except ValueError as e:
            raise f'Produto não cadastrado {e}'
        finally:
            pass
        
    def edit_product(self,*args):
        print(f"{args=}")
        id,produto,quantidade,valor,peso=args
        
        try:
            if len(args)==5:
                #efetua a alteração de ambos os valores
                self.db_client.conn.execute("UPDATE produtos SET produto=?, quantidade=?, valor=?, peso=? WHERE id=?", (produto, quantidade, valor, peso, id))
                self.db_client.conn.commit()
                return f'Produto {self.read_product(id)['id']} atualizado {datetime.today().strftime("%d/%m/%Y")}'

            else:
                if produto!=None:
                    #Efetua a alteração do nome
                    self.db_client.conn.execute("UPDATE produtos SET produto=? WHERE id=?", (produto, id))
                    self.db_client.conn.commit()
                elif quantidade!=None:
                    #Efetua a alteração do email
                    self.db_client.conn.execute("UPDATE produtos SET quantidade=? WHERE id=?", (quantidade,id))
                    self.db_client.conn.commit()
                elif valor!=None:
                    #Efetua a alteração do email
                    self.db_client.conn.execute("UPDATE produtos SET valor=? WHERE id=?", (valor,id))
                    self.db_client.conn.commit()
                elif peso!=None:
                    #Efetua a alteração do email
                    self.db_client.conn.execute("UPDATE produtos SET peso=? WHERE id=?", (peso,id))
                    self.db_client.conn.commit()
                
            return f'Produto {self.read_product(id)['id']} atualizado {datetime.today().strftime("%d/%m/%Y")}'

        except ValueError as e:
            raise f"Erro ao atualizar dados {e}"
        
        finally:
            pass

    def read_product(self, id):
        try:
            row=self.db_client.conn.execute(f"SELECT * FROM produtos WHERE id=?",(id,)).fetchone()
            return dict(row) if row else None 
        except ValueError as e:
            raise f"Erro ao ler produto {e}"
        finally:
            pass
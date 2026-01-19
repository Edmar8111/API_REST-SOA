import db_conn

class ProductRepository:
    def __init__(self,db_client=db_conn.MySQL):
        self.db_client=db_client

    def all_products(self):
        try:
            selectAll=self.db_client.conn.execute(f'SELECT * FROM produtos').fetchall()
            products=[i for i in selectAll]
            return products

        except ValueError as e:
            raise f"Erro ao retornar dados {e}"
    
        finally:
            self.db_client._close()
    
    def delete_product(self, id):
        try:
            self.db_client.conn.execute("DELETE FROM produtos WHERE id=?",(id,))
            self.db_client.conn.commit()
            return 'Produto Deletado'
        except ValueError as e:
            raise f"Erro ao deletar produto {e}"
        finally:
            self.db_client._close()

    def create_product(self,**kwargs):
        user_id,produto,quantidade,valor,peso=(
            kwargs["user_id"], kwargs["produto"],
            kwargs["quantidade"], kwargs["valor"],
            kwargs["peso"]
        )
        try:
            self.db_client.conn.execute('INSERT INTO produtos (user_id, produto, quantidade, valor, peso) VALUES (?, ?, ?, ?, ?)', 
                (user_id, produto, quantidade, valor, peso)
            )
            self.db_client.conn.commit()
            return f'Produto {produto} criado'
        except ValueError as e:
            raise f'Produto não cadastrado {e}'
        finally:
            self.db_client._close()
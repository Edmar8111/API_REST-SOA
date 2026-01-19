import sqlite3
import os

os.environ.setdefault("DATABASE", os.getenv("DATABASE"))

class MySQL:
    def __init__(self, dbConn):
        self.conn = sqlite3.connect()
        if self.conn.is_connected():
            print("Conexão estabelecida.")
            self.cursor=self.conn.cursor()
        self._criar_tabelas()
        
        self.conn.cursor().execute('''
            CREATE TABLE IF NOT EXISTS Container0 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            
            ''')
        self.dbConn.row_factory=sqlite3.Row
        return None
    
    def closeDB(self):
        return self.dbConn.close()
    
    def requestGET(self):
        selectAllQuery=self.dbConn.execute('SELECT * FROM Container0').fetchall()
        dictConver=[dict(user) for user in selectAllQuery]
        return dictConver
    
    def requestPOST(self, name, email):
        try:
            self.dbConn.execute('INSERT INTO Container0 (nome, email) VALUES (?, ?)', (name, email))
            self.dbConn.commit()
            return 'Valor salvo'
        except:
            return 'Valor não salvo'
        
    
    def requestPUT(self,newName,newEmail, id):
        if str(newName).strip()!='' and str(newEmail).strip()!='':
            #efetua a alteração de ambos os valores
            self.dbConn.execute("UPDATE Container0 SET nome=?, email=? WHERE id=?", (newName, newEmail, id))
            self.dbConn.commit()
        elif  str(newName).strip()!='' or str(newEmail).strip()!='':
            if str(newName).strip()!='':
                #Efetua a alteração do nome
                self.dbConn.execute("UPDATE Container0 SET nome=? WHERE id=?", (newName, id))
                self.dbConn.commit()
            else:
                #Efetua a alteração do email
                self.dbConn.execute("UPDATE Container0 SET email=? WHERE id=?", (newEmail,id))
                self.dbConn.commit()
        return 'Dados atualizados'
    
    def requestDELETE(self, id):
        self.dbConn.execute("DELETE FROM Container0 WHERE id=?",(id,))
        self.dbConn.commit()
        return 'Data Delete'
    
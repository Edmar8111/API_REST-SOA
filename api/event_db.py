import sqlite3
import os

DATABASE=os.path.abspath("event_log.db")

class EventLog:
    """
    Docstring for EventLog
    
    funções:
        _close() -> Efetua o fechamento do banco 
        _criar_tabela() -> Instancia as tabelas no banco
        request_get_all() -> Retorna todos os eventos do banco
        create_event(args) -> Cria um evento no banco
    """
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE, timeout=3)
        print("Conexão estabelecida EVENT LOG.")
        self.cursor=self.conn.cursor()
        
        # Retorna linhas como dict-like (acesso por nome de coluna)
        self.conn.row_factory=sqlite3.Row
        
        self._criar_tabelas()
    
    def _close(self):
        return self.conn.close()
    
    def _criar_tabelas(self):

        self.conn.executescript("""
            -- =========================
            -- TABELA: event_log
            -- =========================
            -- "event log: outbox, ibox, retry e data de evento"
            -- Interpretação: tipo_evento com valores permitidos: outbox|ibox|retry
            CREATE TABLE IF NOT EXISTS event_log (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_evento  TEXT    NOT NULL CHECK (tipo_evento IN ('outbox', 'inbox', 'retry')),
                message TEXT DEFAULT NULL,
                data_evento  TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_event_log_tipo_data ON event_log(tipo_evento, data_evento);
        """)
        self.conn.commit()
        
        return 
    
    # Efetua a seleção de todos os dados ativos de uma tabela
    def request_get_all(self):
        try:
            selectAll=self.conn.execute(f'SELECT * FROM event_log').fetchall()
            dictConver=[dict(event) for event in selectAll]
            return dictConver

        except ValueError as e:
            raise f"Erro ao retornar dados {e}"
    
        finally:
            # self._close()
            pass

    def create_event(self, *args):
        msg,kind_event=args
        try:
            self.conn.execute('INSERT INTO event_log (message,tipo_evento) VALUES (?,?)', (msg,kind_event))
            self.conn.commit()
            return f'Evento {kind_event} criado'
        except ValueError as e:
            raise f'Evento não cadastrado {e}'
        finally:
            # self._close()
            pass
    
    

import MySQLdb
import time
import os


os.environ.setdefault("DB_HOST", os.getenv("DB_HOST"))
os.environ.setdefault("DB_PORT", os.getenv("DB_PORT"))
os.environ.setdefault("MYSQL_DATABASE", os.getenv("MYSQL_DATABASE"))
os.environ.setdefault("MYSQL_USER", os.getenv("MYSQL_USER"))
os.environ.setdefault("MYSQL_PASSWORD", os.getenv("MYSQL_PASSWORD"))


class Database:
    """
    Classe responsável por gerenciar a conexão com o banco MySQL
    instanciado dentro do container Docker.

    Esta classe fornece métodos seguros para conexão, execução
    de consultas e encerramento da sessão.
    """

    def __init__(
        self,
        host: str = os.getenv("DB_HOST") or "localhost",
        user: str = os.getenv("MYSQL_USER") or "app_user",
        password: str = os.getenv("MYSQL_PASSWORD") or "app_pass",
        database: str = os.getenv("MYSQL_DATABASE") or "app_db",
        retries: int = 10,
        delay: int = 3
    ) -> None:
        """
        Inicializa a conexão com o banco de dados.

        :param host: Endereço do servidor MySQL
        :param user: Usuário do banco
        :param password: Senha do banco
        :param database: Nome do banco de dados
        :param retries: Tentativas de conexão
        :param delay: Tempo entre tentativas (segundos)
        """
        self.connection = None
        self.cursor = None

        for attempt in range(retries):
            try:
                self.connection = MySQLdb.connect(
                    host=host,
                    user=user,
                    passwd=password,
                    db=database,
                    charset="utf8mb4"
                )
                self.cursor = self.connection.cursor()
                break
            except MySQLdb.OperationalError:
                time.sleep(delay)

        if not self.connection:
            raise ConnectionError("Não foi possível conectar ao MySQL.")
        
    def execute(self, query: str, params: tuple = ()) -> None:
        """
        Executa uma query sem retorno (INSERT, UPDATE, DELETE).

        :param query: Query SQL parametrizada
        :param params: Valores da query
        """
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_one(self, query: str, params: tuple = ()):
        """
        Executa uma query e retorna um único registro.

        :param query: Query SQL parametrizada
        :param params: Valores da query
        :return: Registro encontrado ou None
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()):
        """
        Executa uma query e retorna todos os registros.

        :param query: Query SQL parametrizada
        :param params: Valores da query
        :return: Lista de registros
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self) -> None:
        """
        Encerra a conexão com o banco de dados.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

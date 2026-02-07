import pymysql
from pymysql.err import MySQLError
import pymysql.cursors
import time
import os


os.environ["DB_HOST"] = str(os.getenv("DB_HOST"))

os.environ["DB_PORT"] = os.getenv("DB_PORT")
os.environ["MYSQL_DATABASE"] = str(os.getenv("MYSQL_DATABASE"))
os.environ["MYSQL_USER"] = str(os.getenv("MYSQL_USER"))
os.environ["MYSQL_PASSWORD"] = str(os.getenv("MYSQL_PASSWORD"))

# os.environ.setdefault("DB_HOST", os.getenv("DB_HOST"))
# os.environ.setdefault("DB_PORT", os.getenv("DB_PORT"))
# os.environ.setdefault("MYSQL_DATABASE", os.getenv("MYSQL_DATABASE"))
# os.environ.setdefault("MYSQL_USER", os.getenv("MYSQL_USER"))
# os.environ.setdefault("MYSQL_PASSWORD", os.getenv("MYSQL_PASSWORD"))

class Database:
    """
    Classe responsável por gerenciar a conexão com o banco MySQL
    instanciado dentro do container Docker.

    Esta classe fornece métodos seguros para conexão, execução
    de consultas e encerramento da sessão.
    """

    def __init__(
        self,
        host: str = os.getenv("DB_HOST") or "0.0.0.0",
        user: str = os.getenv("MYSQL_USER") or "app_user",
        password: str = os.getenv("MYSQL_PASSWORD") or "app_pass",
        database: str = os.getenv("MYSQL_DATABASE") or "database",
        retries: int = 10,
        delay: int = 3,
        port: int = 3306,
    ) -> None:
        print("BANCO INICIALIZADO...")
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

        for retry, attempt in enumerate(range(retries)):
            try:
                print(f"Try -> {retry} Connection -> {self.connection}")
                print(f"{pymysql=}")   
                self.connection = pymysql.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=port,
                    # charset="utf8mb4",
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=False,
                )
                self.cursor = self.connection.cursor()  
                break
            except MySQLError as e:
                print(f"Error {e}")
                time.sleep(delay)
                continue

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

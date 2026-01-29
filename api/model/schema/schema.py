"""Módulo de definição da estrutura (schema) do banco de dados."""

def get_setup_script() -> str:
    """
    Retorna o script SQL para criação das tabelas usuario e produtos.
    
    :return: String contendo múltiplas queries SQL.
    """
    return """
    -- Tabela de Usuários
    CREATE TABLE IF NOT EXISTS usuario (
        id            INTEGER AUTO_INCREMENT PRIMARY KEY,
        username      VARCHAR(100) NOT NULL UNIQUE,
        email         VARCHAR(150) NOT NULL UNIQUE,
        data_criacao  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;

    -- Tabela de Produtos
    CREATE TABLE IF NOT EXISTS produtos (
        id         INTEGER AUTO_INCREMENT PRIMARY KEY,
        user_id    INTEGER NOT NULL,
        produto    VARCHAR(100) NOT NULL,
        quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
        valor      DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (valor >= 0),
        peso       DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (peso >= 0),
        CONSTRAINT fk_produtos_usuario
            FOREIGN KEY (user_id)
            REFERENCES usuario(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    ) ENGINE=InnoDB;

    CREATE INDEX id_produtos_user_id ON produtos(user_id);
    """

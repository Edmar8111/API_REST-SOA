# Imagem base oficial do Python (leve e estável)
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /api

# Evita criação de arquivos .pyc e ativa logs imediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV MYSQL_ROOT_PASSWORD=root_pass
ENV MYSQL_DATABASE=database
ENV MYSQL_USER=app_user
ENV MYSQL_PASSWORD=app_pass

# App
ENV DB_HOST=mysql
ENV DB_PORT=3306

# Copia o arquivo de dependências primeiro (boa prática para cache)
COPY /api/requirements.txt .

# Instala dependências de build exigidas pelo mysqlclient
RUN apt-get update && apt-get install -y \
gcc \
pkg-config \
default-libmysqlclient-dev \
&& rm -rf /var/lib/apt/lists/*

# Instala dependências do projeto

RUN pip install --upgrade pip; \
    pip install --no-cache-dir -r requirements.txt

# RUN pip uninstall PyMySQL; \
#     pip install --upgrade PyMySQL

# # Copia todo o código da aplicação para o container

COPY . .


# Expõe a porta padrão do Uvicorn
# EXPOSE 8000

# Comando EXATO solicitado para iniciar a aplicação ASGI
# CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000"]
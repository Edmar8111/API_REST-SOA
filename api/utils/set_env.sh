#!/bin/sh
# ==========================================
# Script de exportação de variáveis de ambiente
# Torna as variáveis globais na sessão atual
# ==========================================

# Definição das variáveis de ambiente
export MYSQL_ROOT_PASSWORD="root_pass"
export MYSQL_DATABASE="app_db"
export MYSQL_USER="app_user"
export MYSQL_PASSWORD="app_pass"

export DB_HOST="mysql"
export DB_PORT="3306"

echo "Variáveis de ambiente carregadas com sucesso:"
env | grep -E "MYSQL_|DB_"

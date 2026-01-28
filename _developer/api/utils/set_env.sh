#!/bin/sh
# ==========================================
# Script de exportação de variáveis de ambiente
# Torna as variáveis globais na sessão atual
# ==========================================

# ----------------------
# MySQL
# ----------------------
export MYSQL_ROOT_PASS="root_pass"
export MYSQL_DATABASE="app_db"
export MYSQL_USER="app_user"
export MYSQL_PASS="app_pass"

# ----------------------
# App
# ----------------------
export DB_HOST="mysql"
export DB_PORT="3306"

# ----------------------
# Feedback visual
# ----------------------
echo "Variáveis de ambiente carregadas com sucesso:"
env | grep -E "MYSQL_|DB_"

#!/usr/bin/env python
"""Script para criar o banco de dados com todas as tabelas"""
import os
import sys

# Mudar para o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Remover banco antigo
db_file = 'estoque_web.db'
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"✓ Banco antigo removido: {db_file}")

# Importar Flask app
from app import app, db

# Criar contexto e tabelas
with app.app_context():
    print("Criando tabelas...")
    db.create_all()
    print("✓ Tabelas criadas com sucesso!")
    
    # Verificar se o arquivo foi criado
    if os.path.exists(db_file):
        print(f"✓ Arquivo de banco criado: {db_file}")
        print(f"  Tamanho: {os.path.getsize(db_file)} bytes")
    else:
        print("✗ Erro: Arquivo de banco não foi criado!")
        sys.exit(1)
    
    # Listar tabelas
    import sqlite3
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tabelas = cursor.fetchall()
    
    if tabelas:
        print(f"\n✓ {len(tabelas)} tabelas criadas:")
        for t in tabelas:
            print(f"  - {t[0]}")
    else:
        print("\n✗ Nenhuma tabela foi criada!")
        sys.exit(1)
    
    conn.close()

print("\n✓ Banco de dados configurado com sucesso!")

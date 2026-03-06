#!/usr/bin/env python
"""Script para criar um banco de dados completamente novo"""
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Remover todos os bancos antigos
for db_file in ['estoque_web.db', '../instance/estoque_web.db']:
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print(f"✓ Removido: {db_file}")
        except Exception as e:
            print(f"✗ Erro ao remover {db_file}: {e}")

# Importar e criar novo banco
from app import app, db

with app.app_context():
    print("\nCriando novo banco com estrutura correta...")
    db.create_all()
    print("✓ Banco criado!")
    
    # Verificar
    import sqlite3
    
    # Procurar o banco
    db_path = None
    for path in ['estoque_web.db', '../instance/estoque_web.db']:
        if os.path.exists(path):
            db_path = path
            break
    
    if db_path:
        print(f"\n✓ Banco encontrado em: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Listar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tabelas = cursor.fetchall()
        print(f"\n✓ {len(tabelas)} tabelas criadas:")
        for t in tabelas:
            print(f"  - {t[0]}")
        
        # Verificar colunas de fornecedores
        print("\nColunas de fornecedores:")
        cursor.execute("PRAGMA table_info(fornecedores)")
        colunas = cursor.fetchall()
        for col in colunas:
            print(f"  - {col[1]} ({col[2]})")
        
        # Verificar colunas de funcionarios
        print("\nColunas de funcionarios:")
        cursor.execute("PRAGMA table_info(funcionarios)")
        colunas = cursor.fetchall()
        for col in colunas:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
    else:
        print("✗ Banco não foi criado!")
        sys.exit(1)

print("\n✓ Banco de dados pronto!")

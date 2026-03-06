#!/usr/bin/env python
"""Criar banco de dados novo e limpo"""
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Importar e criar
from app import app, db

with app.app_context():
    print("Criando banco de dados novo...")
    db.create_all()
    print("✓ Banco criado com sucesso!")
    
    # Verificar
    import sqlite3
    
    # Procurar o banco
    db_path = None
    for path in ['estoque_web.db', 'instance/estoque_web.db']:
        if os.path.exists(path):
            db_path = path
            break
    
    if db_path:
        print(f"✓ Banco encontrado em: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Listar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tabelas = cursor.fetchall()
        print(f"\n✓ {len(tabelas)} tabelas criadas:")
        for t in tabelas:
            print(f"  - {t[0]}")
        
        conn.close()
    else:
        print("✗ Banco não foi criado!")
        sys.exit(1)

print("\n✓ Banco de dados pronto para uso!")

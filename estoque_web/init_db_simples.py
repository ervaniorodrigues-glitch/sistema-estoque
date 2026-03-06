#!/usr/bin/env python
import os
from app import app, db

# Remover banco antigo
db_path = 'estoque_web.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Banco antigo removido")

# Criar contexto
with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")
    
    # Verificar
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tabelas = cursor.fetchall()
    
    print("\nTabelas:")
    for t in tabelas:
        print(f"  - {t[0]}")
    
    conn.close()

#!/usr/bin/env python
"""Script para resetar o banco de dados"""
import os
import sys
import shutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Remover banco antigo
if os.path.exists('estoque_web.db'):
    try:
        os.remove('estoque_web.db')
        print("✓ Banco antigo removido")
    except:
        print("✗ Não foi possível remover o banco antigo")

# Importar e criar novo banco
from app import app, db

with app.app_context():
    print("Criando novo banco...")
    db.create_all()
    print("✓ Novo banco criado!")
    
    # Copiar de instance se necessário
    if os.path.exists('../instance/estoque_web.db'):
        try:
            shutil.copy2('../instance/estoque_web.db', 'estoque_web.db')
            print("✓ Banco copiado de instance/")
        except:
            pass
    
    # Verificar
    import sqlite3
    if os.path.exists('estoque_web.db'):
        conn = sqlite3.connect('estoque_web.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tabelas = cursor.fetchall()
        print(f"\n✓ {len(tabelas)} tabelas criadas:")
        for t in tabelas:
            print(f"  - {t[0]}")
        conn.close()
    else:
        print("✗ Banco não foi criado em estoque_web.db")
        print("  Procurando em instance/...")
        if os.path.exists('../instance/estoque_web.db'):
            print("  ✓ Encontrado em instance/estoque_web.db")

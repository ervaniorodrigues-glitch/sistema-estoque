#!/usr/bin/env python
import os
import sys

# Adicionar o diretório estoque_web ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'estoque_web'))

# Importar a aplicação
from estoque_web.app import app, db

# Criar contexto da aplicação
with app.app_context():
    # Remover banco antigo se existir
    db_path = 'estoque_web/estoque_web.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Banco antigo removido: {db_path}")
    
    # Criar todas as tabelas
    db.create_all()
    print("Todas as tabelas foram criadas com sucesso!")
    
    # Verificar tabelas criadas
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tabelas = cursor.fetchall()
    
    print("\nTabelas criadas:")
    for tabela in tabelas:
        print(f"  ✓ {tabela[0]}")
    
    conn.close()

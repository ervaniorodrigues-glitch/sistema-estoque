#!/usr/bin/env python
import os
import sys

# Garantir que estamos no diretório correto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Remover banco antigo
if os.path.exists('estoque_web.db'):
    os.remove('estoque_web.db')
    print("Banco antigo removido")

# Importar e criar
from app import app, db, Produto, Funcionario, Fornecedor, Cliente, Usuario, Unidade, Marca, Categoria, Operacao, Emprestimo, Movimentacao, ConfiguracaoSistema

with app.app_context():
    print("Criando tabelas...")
    db.create_all()
    print("✓ Tabelas criadas!")
    
    # Verificar
    import sqlite3
    conn = sqlite3.connect('estoque_web.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tabelas = cursor.fetchall()
    
    print(f"\n✓ Total de {len(tabelas)} tabelas criadas:")
    for t in tabelas:
        print(f"  - {t[0]}")
    
    conn.close()

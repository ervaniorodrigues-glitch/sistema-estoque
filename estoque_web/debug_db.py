#!/usr/bin/env python
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("Diretório atual:", os.getcwd())
print("Arquivos .db antes:", [f for f in os.listdir('.') if f.endswith('.db')])

from app import app, db

print("\nConfigurações do app:")
print(f"  DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
print(f"  TRACK_MODIFICATIONS: {app.config['SQLALCHEMY_TRACK_MODIFICATIONS']}")

with app.app_context():
    print("\nCriando tabelas...")
    try:
        db.create_all()
        print("✓ db.create_all() executado sem erros")
    except Exception as e:
        print(f"✗ Erro ao executar db.create_all(): {e}")
        import traceback
        traceback.print_exc()
    
    print("\nArquivos .db depois:", [f for f in os.listdir('.') if f.endswith('.db')])
    
    # Tentar conectar diretamente
    print("\nTentando conectar ao banco...")
    try:
        from sqlalchemy import text
        result = db.session.execute(text("SELECT 1"))
        print("✓ Conexão bem-sucedida")
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")

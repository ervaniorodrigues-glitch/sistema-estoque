"""
Criar todas as tabelas do banco de dados web
"""
import sys
sys.path.insert(0, 'estoque_web')

from app import app, db

with app.app_context():
    print("🔧 Criando tabelas...")
    db.create_all()
    print("✅ Tabelas criadas com sucesso!")
    
    # Verificar
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tabelas = inspector.get_table_names()
    print(f"\n📋 Tabelas criadas: {tabelas}")

"""
Script para executar a migração de 'oficina' para 'categoria'
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from sqlalchemy import text

def executar_migracao():
    """Executa a migração"""
    with app.app_context():
        try:
            print("Iniciando migração...")
            
            # Renomear a coluna
            db.session.execute(text("""
                ALTER TABLE fornecedores 
                RENAME COLUMN oficina TO categoria
            """))
            
            db.session.commit()
            print("✓ Coluna renomeada com sucesso!")
            
            # Verificar
            resultado = db.session.execute(text("PRAGMA table_info(fornecedores)"))
            colunas = [row[1] for row in resultado]
            
            if 'categoria' in colunas and 'oficina' not in colunas:
                print("✓ Migração concluída com sucesso!")
                print("\nColunas atualizadas:")
                for col in colunas:
                    print(f"  - {col}")
                return True
            else:
                print("✗ Erro na migração!")
                return False
                
        except Exception as e:
            db.session.rollback()
            print(f"✗ Erro: {str(e)}")
            return False

if __name__ == '__main__':
    executar_migracao()

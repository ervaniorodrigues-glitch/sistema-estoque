"""
Script para migrar coluna 'oficina' para 'categoria' no banco de dados
TESTE PRIMEIRO - não vai fazer nada, só vai verificar
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Fornecedor
from sqlalchemy import text

def testar_migracao():
    """Testa se a migração vai funcionar"""
    with app.app_context():
        try:
            # Verificar se a coluna 'oficina' existe
            resultado = db.session.execute(text("PRAGMA table_info(fornecedores)"))
            colunas = [row[1] for row in resultado]
            
            print("Colunas atuais na tabela fornecedores:")
            for col in colunas:
                print(f"  - {col}")
            
            if 'oficina' in colunas:
                print("\n✓ Coluna 'oficina' encontrada")
                
                # Contar quantos fornecedores têm dados em 'oficina'
                count = db.session.query(Fornecedor).filter(Fornecedor.oficina != None).count()
                print(f"✓ {count} fornecedores têm dados em 'oficina'")
                
                # Mostrar alguns exemplos
                exemplos = db.session.query(Fornecedor.nome, Fornecedor.oficina).filter(
                    Fornecedor.oficina != None
                ).limit(5).all()
                
                if exemplos:
                    print("\nExemplos de dados:")
                    for nome, oficina in exemplos:
                        print(f"  - {nome}: {oficina}")
                
                print("\n✓ TESTE OK - Pronto para migração!")
                return True
            else:
                print("\n✗ Coluna 'oficina' NÃO encontrada!")
                return False
                
        except Exception as e:
            print(f"\n✗ Erro: {str(e)}")
            return False

if __name__ == '__main__':
    testar_migracao()

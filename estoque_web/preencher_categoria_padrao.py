"""
Script para preencher categoria padrão em fornecedores sem categoria
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Fornecedor

def preencher_categoria():
    with app.app_context():
        # Encontrar fornecedores sem categoria
        fornecedores = Fornecedor.query.filter(
            (Fornecedor.categoria == None) | (Fornecedor.categoria == '')
        ).all()
        
        print(f"Encontrados {len(fornecedores)} fornecedores sem categoria")
        
        for f in fornecedores:
            f.categoria = "Geral"
            print(f"✓ {f.nome}: Categoria definida como 'Geral'")
        
        db.session.commit()
        print(f"\n✓ {len(fornecedores)} fornecedores atualizados!")

if __name__ == '__main__':
    preencher_categoria()

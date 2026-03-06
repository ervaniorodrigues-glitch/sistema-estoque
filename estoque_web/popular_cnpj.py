"""
Script para popular CNPJs fictícios nos fornecedores existentes
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Fornecedor
import random

def gerar_cnpj_valido():
    """Gera um CNPJ fictício válido"""
    # Formato: XX.XXX.XXX/XXXX-XX
    parte1 = str(random.randint(10, 99))
    parte2 = str(random.randint(100, 999))
    parte3 = str(random.randint(100, 999))
    parte4 = str(random.randint(1000, 9999))
    parte5 = str(random.randint(10, 99))
    
    return f"{parte1}.{parte2}.{parte3}/{parte4}-{parte5}"

def popular_cnpjs():
    with app.app_context():
        fornecedores = Fornecedor.query.filter(
            (Fornecedor.cnpj == None) | (Fornecedor.cnpj == '')
        ).all()
        
        print(f"Encontrados {len(fornecedores)} fornecedores sem CNPJ")
        
        for f in fornecedores:
            f.cnpj = gerar_cnpj_valido()
            print(f"✓ {f.nome}: {f.cnpj}")
        
        db.session.commit()
        print(f"\n✓ {len(fornecedores)} fornecedores atualizados com sucesso!")

if __name__ == '__main__':
    popular_cnpjs()

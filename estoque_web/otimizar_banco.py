#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para otimizar o banco de dados adicionando índices
"""
import sys
sys.path.insert(0, '.')

from app import app, db
from sqlalchemy import text

print("=" * 60)
print("OTIMIZANDO BANCO DE DADOS")
print("=" * 60)

with app.app_context():
    # Adicionar índices nas colunas mais consultadas
    indices = [
        ("fornecedores", "ativo"),
        ("fornecedores", "nome"),
        ("fornecedores", "cnpj"),
        ("funcionarios", "ativo"),
        ("funcionarios", "nome"),
        ("clientes", "ativo"),
        ("clientes", "nome"),
        ("produtos", "ativo"),
        ("produtos", "descricao"),
        ("emprestimos", "cod_produto"),
        ("emprestimos", "status"),
    ]
    
    for tabela, coluna in indices:
        try:
            index_name = f"idx_{tabela}_{coluna}"
            sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {tabela}({coluna})"
            db.session.execute(text(sql))
            print(f"✓ Índice criado: {index_name}")
        except Exception as e:
            print(f"✗ Erro ao criar índice {index_name}: {e}")
    
    db.session.commit()
    print("\n" + "=" * 60)
    print("OTIMIZAÇÃO CONCLUÍDA!")
    print("=" * 60)

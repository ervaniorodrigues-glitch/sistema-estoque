#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')

from app import app, db, Produto, Emprestimo, Funcionario, Fornecedor, Cliente

print("=" * 60)
print("ANÁLISE DE PERFORMANCE - CONTAGEM DE REGISTROS")
print("=" * 60)

with app.app_context():
    produtos = Produto.query.count()
    emprestimos = Emprestimo.query.count()
    funcionarios = Funcionario.query.count()
    fornecedores = Fornecedor.query.count()
    clientes = Cliente.query.count()

    print(f"Produtos: {produtos}")
    print(f"Emprestimos: {emprestimos}")
    print(f"Funcionarios: {funcionarios}")
    print(f"Fornecedores: {fornecedores}")
    print(f"Clientes: {clientes}")

    print("\n" + "=" * 60)
    print("PROBLEMA IDENTIFICADO:")
    print("=" * 60)
    print(f"Na rota /api/produtos, para cada produto ({produtos}),")
    print(f"está fazendo 1 query na tabela Emprestimo.")
    print(f"Total de queries: 1 (listar produtos) + {produtos} (emprestimos) = {1 + produtos} queries!")
    print("\nISSO ESTÁ CAUSANDO A LENTIDÃO!")
    print("=" * 60)

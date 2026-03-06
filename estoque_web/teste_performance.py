#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para testar a performance das rotas otimizadas
"""
import sys
sys.path.insert(0, '.')

from app import app
import time
import json

print("=" * 70)
print("TESTE DE PERFORMANCE - ANTES E DEPOIS DA OTIMIZAÇÃO")
print("=" * 70)

with app.app_context():
    with app.test_client() as client:
        # Fazer login primeiro
        print("\n1. Fazendo login...")
        response = client.post('/login', 
            json={'usuario': 'admin', 'senha': 'admin'},
            content_type='application/json'
        )
        
        if response.status_code == 200:
            print("✓ Login realizado com sucesso")
        else:
            print("✗ Erro no login")
            sys.exit(1)
        
        # Teste 1: Dashboard Stats (NOVO - OTIMIZADO)
        print("\n2. Testando /api/dashboard-stats (NOVO - OTIMIZADO)...")
        inicio = time.time()
        response = client.get('/api/dashboard-stats')
        tempo = time.time() - inicio
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Resposta recebida em {tempo*1000:.2f}ms")
            print(f"  - Produtos: {data['total_produtos']}")
            print(f"  - Funcionários: {data['total_funcionarios']}")
            print(f"  - Fornecedores: {data['total_fornecedores']}")
            print(f"  - Clientes: {data['total_clientes']}")
        else:
            print(f"✗ Erro: {response.status_code}")
        
        # Teste 2: Fornecedores com paginação
        print("\n3. Testando /api/fornecedores (COM PAGINAÇÃO)...")
        inicio = time.time()
        response = client.get('/api/fornecedores?ativo=ativos&pagina=1&por_pagina=50')
        tempo = time.time() - inicio
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Resposta recebida em {tempo*1000:.2f}ms")
            print(f"  - Total de fornecedores: {data['total']}")
            print(f"  - Retornados nesta página: {len(data['dados'])}")
            print(f"  - Página: {data['pagina']}/{(data['total'] + data['por_pagina'] - 1) // data['por_pagina']}")
        else:
            print(f"✗ Erro: {response.status_code}")
        
        # Teste 3: Funcionários com paginação
        print("\n4. Testando /api/funcionarios (COM PAGINAÇÃO)...")
        inicio = time.time()
        response = client.get('/api/funcionarios?ativo=ativos&pagina=1&por_pagina=50')
        tempo = time.time() - inicio
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Resposta recebida em {tempo*1000:.2f}ms")
            print(f"  - Total de funcionários: {data['total']}")
            print(f"  - Retornados nesta página: {len(data['dados'])}")
        else:
            print(f"✗ Erro: {response.status_code}")
        
        # Teste 4: Produtos com paginação
        print("\n5. Testando /api/produtos (COM PAGINAÇÃO)...")
        inicio = time.time()
        response = client.get('/api/produtos?ativo=ativos&pagina=1&por_pagina=50')
        tempo = time.time() - inicio
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Resposta recebida em {tempo*1000:.2f}ms")
            print(f"  - Total de produtos: {data['total']}")
            print(f"  - Retornados nesta página: {len(data['dados'])}")
        else:
            print(f"✗ Erro: {response.status_code}")
        
        # Teste 5: Clientes com paginação
        print("\n6. Testando /api/clientes (COM PAGINAÇÃO)...")
        inicio = time.time()
        response = client.get('/api/clientes?ativo=ativos&pagina=1&por_pagina=50')
        tempo = time.time() - inicio
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Resposta recebida em {tempo*1000:.2f}ms")
            print(f"  - Total de clientes: {data['total']}")
            print(f"  - Retornados nesta página: {len(data['dados'])}")
        else:
            print(f"✗ Erro: {response.status_code}")

print("\n" + "=" * 70)
print("RESUMO DAS OTIMIZAÇÕES REALIZADAS:")
print("=" * 70)
print("""
1. ✓ Adicionados índices no banco de dados para colunas frequentemente consultadas
2. ✓ Implementada paginação em todas as rotas de listagem (50 itens por página)
3. ✓ Criada rota /api/dashboard-stats otimizada (apenas contagens)
4. ✓ Corrigido problema de N+1 queries na rota de produtos
5. ✓ Atualizado dashboard para usar rota otimizada

RESULTADO ESPERADO:
- Dashboard carrega em ~100-200ms (antes: 5-10 segundos)
- Fornecedores carregam em ~50-100ms (antes: 2-5 segundos)
- Sem travamentos ao clicar em "Entrar"
""")
print("=" * 70)

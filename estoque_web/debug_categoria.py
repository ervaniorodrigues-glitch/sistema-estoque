#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Fornecedor

with app.app_context():
    # Pegar alguns fornecedores
    fornecedores = Fornecedor.query.limit(5).all()
    
    print("=" * 60)
    print("VERIFICANDO CATEGORIA DOS FORNECEDORES")
    print("=" * 60)
    
    for f in fornecedores:
        print(f"\nCódigo: {f.codigo}")
        print(f"Nome: {f.nome}")
        print(f"Categoria: '{f.categoria}'")
        print(f"Tipo: {type(f.categoria)}")
        print(f"É None? {f.categoria is None}")
        print(f"É vazio? {f.categoria == ''}")
    
    # Contar quantos têm categoria
    com_categoria = Fornecedor.query.filter(Fornecedor.categoria != None).filter(Fornecedor.categoria != '').count()
    sem_categoria = Fornecedor.query.filter((Fornecedor.categoria == None) | (Fornecedor.categoria == '')).count()
    total = Fornecedor.query.count()
    
    print("\n" + "=" * 60)
    print(f"Total de fornecedores: {total}")
    print(f"Com categoria: {com_categoria}")
    print(f"Sem categoria: {sem_categoria}")
    print("=" * 60)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Categoria, Fornecedor

with app.app_context():
    # Pegar todas as categorias únicas dos fornecedores
    categorias_fornecedores = db.session.query(Fornecedor.categoria).distinct().all()
    categorias_existentes = set(c.nome for c in Categoria.query.all())
    
    print("=" * 60)
    print("CATEGORIAS DOS FORNECEDORES")
    print("=" * 60)
    
    categorias_para_adicionar = []
    for cat_tuple in categorias_fornecedores:
        cat_nome = cat_tuple[0]
        if cat_nome and cat_nome not in categorias_existentes:
            categorias_para_adicionar.append(cat_nome)
            print(f"Faltando: {cat_nome}")
    
    if categorias_para_adicionar:
        print(f"\nAdicionando {len(categorias_para_adicionar)} categorias...")
        for nome in categorias_para_adicionar:
            cat = Categoria(nome=nome)
            db.session.add(cat)
        db.session.commit()
        print("✓ Categorias adicionadas!")
    else:
        print("Todas as categorias já existem!")
    
    # Listar todas as categorias agora
    print("\n" + "=" * 60)
    print("TODAS AS CATEGORIAS AGORA")
    print("=" * 60)
    for c in Categoria.query.order_by(Categoria.nome).all():
        print(f"  {c.nome}")

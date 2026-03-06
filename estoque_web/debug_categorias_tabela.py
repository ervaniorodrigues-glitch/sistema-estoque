#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Categoria

with app.app_context():
    categorias = Categoria.query.all()
    
    print("=" * 60)
    print("CATEGORIAS NO BANCO")
    print("=" * 60)
    print(f"Total: {len(categorias)}\n")
    
    for c in categorias:
        print(f"ID: {c.id} | Nome: {c.nome}")
    
    if len(categorias) == 0:
        print("NENHUMA CATEGORIA ENCONTRADA!")
        print("\nCriando categorias padrão...")
        
        categorias_padrao = ['Ferramenta', 'Mecânica', 'Elétrica', 'Geral']
        for nome in categorias_padrao:
            cat = Categoria(nome=nome)
            db.session.add(cat)
        
        db.session.commit()
        print(f"✓ {len(categorias_padrao)} categorias criadas!")

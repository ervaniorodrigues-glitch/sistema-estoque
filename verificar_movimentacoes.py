#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar as movimentações recentes
"""

import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'estoque.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar movimentações recentes
    cursor.execute("""
        SELECT id, produto_codigo, tipo, quantidade, valor_total, 
               solicitante_nome, data_movimentacao, lote_id
        FROM movimentacoes
        WHERE tipo = 'ENTRADA'
        ORDER BY data_movimentacao DESC
        LIMIT 20
    """)
    
    movimentacoes = cursor.fetchall()
    
    print("Movimentações recentes:")
    print("-" * 100)
    for mov in movimentacoes:
        print(f"ID: {mov[0]:3d} | Produto: {mov[1]:3d} | Qtd: {mov[3]:3d} | "
              f"Valor: R$ {mov[4]:8.2f} | Fornecedor: {mov[5][:30]:30s} | "
              f"Data: {mov[6]} | Lote: {mov[7]}")
    
    conn.close()
    
except Exception as e:
    print(f"Erro: {e}")

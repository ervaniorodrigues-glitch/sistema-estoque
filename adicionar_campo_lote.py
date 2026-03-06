#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para adicionar campo lote_id na tabela movimentacoes
Isso permitirá agrupar entradas múltiplas no relatório
"""

import sqlite3
import os

# Caminho do banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'estoque.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar se a coluna já existe
    cursor.execute("PRAGMA table_info(movimentacoes)")
    colunas = [col[1] for col in cursor.fetchall()]
    
    if 'lote_id' not in colunas:
        print("Adicionando coluna lote_id...")
        cursor.execute("ALTER TABLE movimentacoes ADD COLUMN lote_id VARCHAR(50)")
        conn.commit()
        print("✓ Coluna lote_id adicionada com sucesso!")
    else:
        print("✓ Coluna lote_id já existe!")
    
    conn.close()
    print("\n✓ Migração concluída!")
    
except Exception as e:
    print(f"✗ Erro: {e}")

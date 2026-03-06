#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar colunas solicitante_tipo e solicitante_nome na tabela movimentacoes
"""

import sqlite3
import os

# Caminho do banco de dados (estoque_web.db)
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'estoque_web.db')

print(f"Conectando ao banco: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar se as colunas já existem
    cursor.execute("PRAGMA table_info(movimentacoes)")
    colunas = [col[1] for col in cursor.fetchall()]
    
    print(f"Colunas atuais: {colunas}")
    
    # Adicionar coluna solicitante_tipo se não existir
    if 'solicitante_tipo' not in colunas:
        print("Adicionando coluna solicitante_tipo...")
        cursor.execute("ALTER TABLE movimentacoes ADD COLUMN solicitante_tipo VARCHAR(50)")
        print("✓ Coluna solicitante_tipo adicionada!")
    else:
        print("✓ Coluna solicitante_tipo já existe")
    
    # Adicionar coluna solicitante_nome se não existir
    if 'solicitante_nome' not in colunas:
        print("Adicionando coluna solicitante_nome...")
        cursor.execute("ALTER TABLE movimentacoes ADD COLUMN solicitante_nome VARCHAR(200)")
        print("✓ Coluna solicitante_nome adicionada!")
    else:
        print("✓ Coluna solicitante_nome já existe")
    
    conn.commit()
    print("\n✅ Migração concluída com sucesso!")
    
except Exception as e:
    print(f"\n❌ Erro ao adicionar colunas: {e}")
    
finally:
    if conn:
        conn.close()

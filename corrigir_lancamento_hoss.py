#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para corrigir o lançamento da entrada múltipla
Agrupa as movimentações do dia 05/03/2026 em um único lote
"""

import sqlite3
import os
from datetime import datetime

# Caminho do banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'estoque.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar movimentações do dia 05/03/2026 com o mesmo timestamp (entrada múltipla)
    cursor.execute("""
        SELECT id, produto_codigo, quantidade, valor_total, data_movimentacao, solicitante_nome
        FROM movimentacoes
        WHERE tipo = 'ENTRADA'
        AND data_movimentacao LIKE '2026-03-05 10:14:%'
        AND (lote_id IS NULL OR lote_id = '')
        ORDER BY id
    """)
    
    movimentacoes = cursor.fetchall()
    
    if not movimentacoes:
        print("✗ Nenhuma movimentação encontrada para corrigir")
        conn.close()
        exit()
    
    print(f"Encontradas {len(movimentacoes)} movimentações para agrupar:")
    total_valor = 0
    for mov in movimentacoes:
        print(f"  - ID: {mov[0]}, Produto: {mov[1]}, Qtd: {mov[2]}, Valor: R$ {mov[3]:.2f}, Fornecedor: {mov[5]}")
        total_valor += mov[3]
    
    print(f"\nValor total: R$ {total_valor:.2f}")
    
    # Gerar lote_id único
    lote_id = f"LOTE_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Atualizar todas as movimentações com o mesmo lote_id
    ids = [str(mov[0]) for mov in movimentacoes]
    cursor.execute(f"""
        UPDATE movimentacoes
        SET lote_id = ?, solicitante_nome = 'Hoss Contrutora Ltda*'
        WHERE id IN ({','.join(ids)})
    """, (lote_id,))
    
    conn.commit()
    
    print(f"\n✓ {len(movimentacoes)} movimentações agrupadas com sucesso!")
    print(f"✓ Lote ID: {lote_id}")
    print(f"✓ Fornecedor atualizado para: Hoss Contrutora Ltda*")
    print(f"✓ Agora aparecerão como uma única entrada no relatório")
    
    conn.close()
    
except Exception as e:
    print(f"✗ Erro: {e}")

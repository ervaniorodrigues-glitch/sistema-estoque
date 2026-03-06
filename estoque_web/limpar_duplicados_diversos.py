#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para remover duplicados das tabelas de cadastros diversos
Remove itens duplicados considerando case-insensitive
"""

import sqlite3
from collections import defaultdict

def limpar_duplicados():
    conn = sqlite3.connect('estoque_web/estoque_web.db')
    cursor = conn.cursor()
    
    tabelas = ['unidades', 'marcas', 'categorias', 'operacoes']
    
    for tabela in tabelas:
        print(f"\n{'='*60}")
        print(f"Limpando duplicados em: {tabela.upper()}")
        print('='*60)
        
        # Buscar todos os registros
        cursor.execute(f"SELECT id, nome FROM {tabela}")
        registros = cursor.fetchall()
        
        # Agrupar por nome (case-insensitive)
        grupos = defaultdict(list)
        for id_reg, nome in registros:
            grupos[nome.lower()].append((id_reg, nome))
        
        # Remover duplicados (manter apenas o primeiro)
        removidos = 0
        for nome_lower, items in grupos.items():
            if len(items) > 1:
                print(f"\n❌ Duplicados encontrados para '{items[0][1]}':")
                # Manter o primeiro, remover os outros
                for i, (id_reg, nome_original) in enumerate(items):
                    if i == 0:
                        print(f"   ✓ Mantendo: {nome_original} (ID: {id_reg})")
                    else:
                        print(f"   🗑️  Removendo: {nome_original} (ID: {id_reg})")
                        cursor.execute(f"DELETE FROM {tabela} WHERE id = ?", (id_reg,))
                        removidos += 1
        
        if removidos == 0:
            print(f"✅ Nenhum duplicado encontrado em {tabela}")
        else:
            print(f"\n✅ Total removido: {removidos} registro(s)")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*60}")
    print("✅ LIMPEZA CONCLUÍDA!")
    print('='*60)

if __name__ == '__main__':
    limpar_duplicados()

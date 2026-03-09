"""
Script para migrar dados do SQLite local para PostgreSQL no Render
Execute este script LOCALMENTE para exportar os dados
"""

import sqlite3
import json
from datetime import datetime

def exportar_dados_sqlite(db_path='estoque.db'):
    """Exporta todos os dados do SQLite para JSON"""
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    dados = {}
    
    # Lista de tabelas para exportar
    tabelas = [
        'usuario',
        'produto',
        'fornecedor',
        'cliente',
        'funcionario',
        'movimentacao',
        'emprestimo',
        'unidade_div',
        'marca_div',
        'categoria_div',
        'operacao_div',
        'anos_div'
    ]
    
    print("🔄 Exportando dados do SQLite...")
    
    for tabela in tabelas:
        try:
            cursor.execute(f"SELECT * FROM {tabela}")
            rows = cursor.fetchall()
            dados[tabela] = [dict(row) for row in rows]
            print(f"✅ {tabela}: {len(rows)} registros")
        except sqlite3.OperationalError as e:
            print(f"⚠️  {tabela}: Tabela não existe ou erro - {e}")
            dados[tabela] = []
    
    conn.close()
    
    # Salvar em arquivo JSON
    filename = f'backup_sqlite_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ Dados exportados para: {filename}")
    print(f"📊 Total de tabelas: {len([t for t in dados if dados[t]])}")
    print(f"📝 Total de registros: {sum(len(dados[t]) for t in dados)}")
    
    return filename

if __name__ == '__main__':
    print("="*60)
    print("MIGRAÇÃO SQLite → PostgreSQL")
    print("="*60)
    print()
    
    # Exportar dados
    arquivo = exportar_dados_sqlite()
    
    print()
    print("="*60)
    print("PRÓXIMOS PASSOS:")
    print("="*60)
    print(f"1. O arquivo '{arquivo}' foi criado")
    print("2. Você precisa criar um script de importação no Render")
    print("3. Ou importar os dados manualmente através da interface web")
    print()
    print("⚠️  IMPORTANTE:")
    print("- Backup do SQLite não é compatível com PostgreSQL")
    print("- Use este arquivo JSON para importar os dados")
    print("="*60)

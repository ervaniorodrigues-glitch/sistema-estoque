"""
Script para exportar TODOS os dados do SQLite local para SQL PostgreSQL
"""

import sqlite3
import os
from datetime import datetime

# Caminho do banco SQLite
DB_PATH = 'instance/estoque.db'

def exportar_dados():
    """Exporta todos os dados do SQLite para SQL PostgreSQL"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco não encontrado: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Descobrir todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tabelas = [row[0] for row in cursor.fetchall()]
    
    print("="*60)
    print("EXPORTAÇÃO DE DADOS - SQLite → PostgreSQL")
    print("="*60)
    print(f"Banco: {DB_PATH}")
    print(f"Tabelas encontradas: {len(tabelas)}")
    print()
    
    output_sql = []
    output_sql.append("-- Migração de dados SQLite para PostgreSQL")
    output_sql.append(f"-- Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_sql.append(f"-- Banco origem: {DB_PATH}")
    output_sql.append("")
    
    total_registros = 0
    
    for tabela in sorted(tabelas):
        try:
            # Pegar estrutura da tabela
            cursor.execute(f"PRAGMA table_info({tabela})")
            colunas_info = cursor.fetchall()
            colunas = [col[1] for col in colunas_info]
            
            # Pegar dados
            cursor.execute(f"SELECT * FROM {tabela}")
            rows = cursor.fetchall()
            
            if rows:
                print(f"✅ {tabela}: {len(rows)} registros")
                
                output_sql.append(f"\n-- Tabela: {tabela}")
                output_sql.append(f"-- Colunas: {', '.join(colunas)}")
                
                for row in rows:
                    valores = []
                    for i, col in enumerate(colunas):
                        try:
                            valor = row[col]
                        except:
                            valor = None
                        
                        # Verificar se a coluna é booleana (ativo, admin, etc)
                        col_lower = col.lower()
                        is_boolean = col_lower in ['ativo', 'admin']
                        
                        if valor is None:
                            valores.append('NULL')
                        elif is_boolean:
                            # Converter 0/1 para FALSE/TRUE
                            if valor in (0, '0', False):
                                valores.append('FALSE')
                            else:
                                valores.append('TRUE')
                        elif isinstance(valor, bool):
                            valores.append('TRUE' if valor else 'FALSE')
                        elif isinstance(valor, (int, float)):
                            valores.append(str(valor))
                        else:
                            # Escapar aspas simples e caracteres especiais
                            valor_str = str(valor).replace("'", "''").replace('\n', ' ').replace('\r', '')
                            
                            # Truncar campos específicos que têm limite de tamanho
                            if col_lower == 'uf' and len(valor_str) > 2:
                                valor_str = valor_str[:2]  # Truncar UF para 2 caracteres
                            elif col_lower == 'cep' and len(valor_str) > 10:
                                valor_str = valor_str[:10]
                            elif col_lower == 'cpfcnpj' and len(valor_str) > 18:
                                valor_str = valor_str[:18]
                            elif col_lower == 'telefone' and len(valor_str) > 20:
                                valor_str = valor_str[:20]
                            elif col_lower == 'celular' and len(valor_str) > 20:
                                valor_str = valor_str[:20]
                            
                            valores.append(f"'{valor_str}'")
                    
                    sql = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({', '.join(valores)});"
                    output_sql.append(sql)
                
                # Resetar sequence se a tabela tiver coluna id
                if 'id' in colunas:
                    output_sql.append(f"SELECT setval(pg_get_serial_sequence('{tabela}', 'id'), COALESCE((SELECT MAX(id) FROM {tabela}), 1), true);")
                
                output_sql.append("")
                total_registros += len(rows)
            else:
                print(f"⚠️  {tabela}: Sem registros")
                
        except Exception as e:
            print(f"❌ {tabela}: Erro - {e}")
    
    conn.close()
    
    # Salvar arquivo SQL
    filename = f'migracao_completa_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_sql))
    
    print()
    print("="*60)
    print(f"✅ Arquivo SQL gerado: {filename}")
    print(f"📊 Total de tabelas exportadas: {len([t for t in tabelas])}")
    print(f"📝 Total de registros: {total_registros}")
    print("="*60)
    print()
    print("PRÓXIMOS PASSOS:")
    print("1. Copie o conteúdo do arquivo SQL")
    print("2. Acesse o Render e vá no banco PostgreSQL")
    print("3. Execute o SQL no banco de dados")
    print("="*60)
    
    return filename

if __name__ == '__main__':
    try:
        exportar_dados()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()

"""
Script para exportar dados do SQLite e gerar SQL para PostgreSQL
Execute este script LOCALMENTE
"""

import sqlite3
import json
from datetime import datetime

def exportar_para_sql_postgres(db_path='instance/estoque.db'):
    """Exporta dados do SQLite e gera SQL para PostgreSQL"""
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    output_sql = []
    output_sql.append("-- Migração de dados SQLite para PostgreSQL")
    output_sql.append(f"-- Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_sql.append("")
    
    # Lista de tabelas para exportar (na ordem correta para evitar problemas de FK)
    tabelas = [
        ('usuario', ['id', 'usuario', 'senha', 'nome', 'admin', 'tipo', 'ativo']),
        ('unidade_div', ['id', 'nome']),
        ('marca_div', ['id', 'nome']),
        ('categoria_div', ['id', 'nome']),
        ('operacao_div', ['id', 'nome']),
        ('anos_div', ['id', 'ano']),
        ('fornecedor', ['id', 'nome', 'cpf_cnpj', 'telefone', 'email', 'endereco', 'ativo']),
        ('cliente', ['id', 'nome', 'cpf_cnpj', 'telefone', 'email', 'endereco', 'ativo']),
        ('funcionario', ['id', 'nome', 'cpf', 'telefone', 'email', 'cargo', 'ativo']),
        ('produto', ['id', 'nome', 'descricao', 'unidade', 'marca', 'categoria', 'preco_compra', 'preco_venda', 'estoque_minimo', 'estoque_atual', 'fornecedor_id', 'imagem', 'ativo']),
        ('movimentacao', ['id', 'produto_id', 'tipo', 'quantidade', 'preco_unitario', 'valor_total', 'operacao', 'fornecedor_id', 'cliente_id', 'solicitante_tipo', 'solicitante_nome', 'observacao', 'data_movimentacao', 'usuario_id']),
        ('emprestimo', ['id', 'produto_id', 'funcionario_id', 'quantidade', 'status', 'data_devolucao_prevista', 'data_devolucao', 'data_cadastro']),
    ]
    
    print("🔄 Exportando dados do SQLite para SQL PostgreSQL...")
    print()
    
    total_registros = 0
    
    for tabela, colunas in tabelas:
        try:
            cursor.execute(f"SELECT * FROM {tabela}")
            rows = cursor.fetchall()
            
            if rows:
                print(f"✅ {tabela}: {len(rows)} registros")
                
                # Desabilitar triggers temporariamente
                output_sql.append(f"\n-- Tabela: {tabela}")
                output_sql.append(f"DELETE FROM {tabela};")
                
                for row in rows:
                    valores = []
                    for col in colunas:
                        valor = row[col] if col in row.keys() else None
                        
                        if valor is None:
                            valores.append('NULL')
                        elif isinstance(valor, (int, float)):
                            valores.append(str(valor))
                        elif isinstance(valor, bool):
                            valores.append('TRUE' if valor else 'FALSE')
                        else:
                            # Escapar aspas simples
                            valor_str = str(valor).replace("'", "''")
                            valores.append(f"'{valor_str}'")
                    
                    sql = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({', '.join(valores)});"
                    output_sql.append(sql)
                
                # Resetar sequence do ID
                output_sql.append(f"SELECT setval(pg_get_serial_sequence('{tabela}', 'id'), COALESCE((SELECT MAX(id) FROM {tabela}), 1));")
                output_sql.append("")
                
                total_registros += len(rows)
            else:
                print(f"⚠️  {tabela}: Sem registros")
                
        except sqlite3.OperationalError as e:
            print(f"❌ {tabela}: Erro - {e}")
    
    conn.close()
    
    # Salvar arquivo SQL
    filename = f'migracao_postgres_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_sql))
    
    print()
    print("="*60)
    print(f"✅ Arquivo SQL gerado: {filename}")
    print(f"📊 Total de tabelas: {len([t for t, _ in tabelas])}")
    print(f"📝 Total de registros: {total_registros}")
    print("="*60)
    
    return filename

if __name__ == '__main__':
    print("="*60)
    print("EXPORTAÇÃO SQLite → PostgreSQL")
    print("="*60)
    print()
    
    try:
        arquivo = exportar_para_sql_postgres()
        
        print()
        print("PRÓXIMOS PASSOS:")
        print("="*60)
        print(f"1. Abra o arquivo: {arquivo}")
        print("2. Copie todo o conteúdo")
        print("3. No Render, vá em 'Shell' do PostgreSQL")
        print("4. Execute o comando: psql $DATABASE_URL")
        print("5. Cole o conteúdo do arquivo SQL")
        print("6. Aguarde a importação completar")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

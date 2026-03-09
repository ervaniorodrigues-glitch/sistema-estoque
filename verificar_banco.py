import sqlite3

conn = sqlite3.connect('instance/estoque.db')
cursor = conn.cursor()

tabelas = ['produtos', 'fornecedores', 'funcionarios', 'clientes', 'usuarios']

print('='*50)
print('DADOS REAIS NO BANCO SQLite:')
print('='*50)

for tabela in tabelas:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
        count = cursor.fetchone()[0]
        print(f'{tabela}: {count} registros')
    except Exception as e:
        print(f'{tabela}: ERRO - {e}')

conn.close()

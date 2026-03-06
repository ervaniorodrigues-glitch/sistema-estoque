import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

print('=' * 80)
print('COLUNAS DA TABELA ENTRADAS_ESTOQUE:')
print('=' * 80)
cursor.execute('PRAGMA table_info(entradas_estoque)')
for col in cursor.fetchall():
    print(f'{col[1]} ({col[2]})')

print()
print('=' * 80)
print('COLUNAS DA TABELA SAIDAS_ESTOQUE:')
print('=' * 80)
cursor.execute('PRAGMA table_info(saidas_estoque)')
for col in cursor.fetchall():
    print(f'{col[1]} ({col[2]})')

conn.close()

import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

cursor.execute('SELECT data, funcionario, descricao_item, status FROM emprestimos ORDER BY data')

print('=' * 80)
print('TODOS OS EMPRÉSTIMOS NO BANCO:')
print('=' * 80)
print()

for r in cursor.fetchall():
    print(f'{r[0]} | {r[1]} | {r[2]} | {r[3]}')

conn.close()

import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

cursor.execute("SELECT codigo, descricao, estoque_atual FROM produtos ORDER BY codigo")
produtos = cursor.fetchall()

print('=== TODOS OS PRODUTOS ===')
for p in produtos:
    print(f'Código: {p[0]}, Descrição: {p[1]}, Estoque: {p[2]}')

conn.close()

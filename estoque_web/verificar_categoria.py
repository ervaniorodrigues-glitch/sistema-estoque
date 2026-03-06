import sqlite3
import os

# Encontrar o banco de dados
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estoque.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verificar quantos têm categoria vazia
cursor.execute('SELECT COUNT(*) FROM fornecedores WHERE categoria IS NULL OR categoria = ""')
sem_categoria = cursor.fetchone()[0]
print(f'Fornecedores sem categoria: {sem_categoria}')

# Ver alguns exemplos
cursor.execute('SELECT codigo, nome, categoria FROM fornecedores LIMIT 10')
print('\nExemplos:')
for row in cursor.fetchall():
    print(f'  {row[0]}: {row[1]} -> {row[2]}')

# Preencher com valor padrão
if sem_categoria > 0:
    cursor.execute('UPDATE fornecedores SET categoria = "Geral" WHERE categoria IS NULL OR categoria = ""')
    conn.commit()
    print(f'\n✓ {cursor.rowcount} fornecedores atualizados com categoria "Geral"')

conn.close()

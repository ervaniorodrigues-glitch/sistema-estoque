import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estoque.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ver a estrutura da tabela produtos
cursor.execute("PRAGMA table_info(produtos)")
print("Colunas da tabela produtos:")
for col in cursor.fetchall():
    print(f"  {col[1]}: {col[2]}")

# Ver um produto de exemplo
cursor.execute("SELECT * FROM produtos LIMIT 1")
cols = [description[0] for description in cursor.description]
row = cursor.fetchone()
if row:
    print("\nExemplo de produto:")
    for col, val in zip(cols, row):
        print(f"  {col}: {val}")

conn.close()

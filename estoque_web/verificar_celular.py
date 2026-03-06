import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estoque.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== VERIFICANDO CAMPO CELULAR ===\n")

# Ver estrutura
cursor.execute("PRAGMA table_info(funcionarios)")
print("Colunas da tabela funcionarios:")
for col in cursor.fetchall():
    print(f"  {col[1]}: {col[2]}")

# Ver dados
cursor.execute("SELECT id, nome, celular FROM funcionarios LIMIT 5")
print("\nExemplos de funcionários:")
for row in cursor.fetchall():
    print(f"  ID {row[0]}: {row[1]} -> Celular: {row[2]}")

conn.close()

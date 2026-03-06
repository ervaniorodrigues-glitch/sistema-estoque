import sqlite3

conn = sqlite3.connect('estoque_web/estoque_web.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = cursor.fetchall()

print("Tabelas no banco:")
for t in tabelas:
    print(f"  - {t[0]}")

# Verificar colunas da tabela fornecedores
print("\nColunas da tabela fornecedores:")
cursor.execute("PRAGMA table_info(fornecedores)")
colunas = cursor.fetchall()
for col in colunas:
    print(f"  - {col[1]} ({col[2]})")

# Verificar colunas da tabela funcionarios
print("\nColunas da tabela funcionarios:")
cursor.execute("PRAGMA table_info(funcionarios)")
colunas = cursor.fetchall()
for col in colunas:
    print(f"  - {col[1]} ({col[2]})")

conn.close()

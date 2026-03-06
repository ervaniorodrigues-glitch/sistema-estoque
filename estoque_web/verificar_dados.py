import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estoque.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== VERIFICANDO DADOS ===\n")

# Verificar unidades
cursor.execute("SELECT COUNT(*) FROM unidades_div")
print(f"Unidades: {cursor.fetchone()[0]}")
cursor.execute("SELECT nome FROM unidades_div LIMIT 5")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

# Verificar marcas
cursor.execute("SELECT COUNT(*) FROM marcas_div")
print(f"\nMarcas: {cursor.fetchone()[0]}")
cursor.execute("SELECT nome FROM marcas_div LIMIT 5")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

# Verificar categorias
cursor.execute("SELECT COUNT(*) FROM categorias_div")
print(f"\nCategorias: {cursor.fetchone()[0]}")
cursor.execute("SELECT nome FROM categorias_div LIMIT 5")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

# Verificar fornecedores
cursor.execute("SELECT COUNT(*) FROM fornecedores")
print(f"\nFornecedores: {cursor.fetchone()[0]}")
cursor.execute("SELECT nome FROM fornecedores LIMIT 5")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

conn.close()

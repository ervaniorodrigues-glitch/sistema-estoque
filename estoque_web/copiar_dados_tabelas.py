import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estoque.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== COPIANDO DADOS ENTRE TABELAS ===\n")

# Copiar unidades
try:
    cursor.execute("INSERT OR IGNORE INTO unidades (nome) SELECT nome FROM unidades_div")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM unidades")
    print(f"✓ Unidades: {cursor.fetchone()[0]}")
except Exception as e:
    print(f"✗ Erro ao copiar unidades: {e}")

# Copiar marcas
try:
    cursor.execute("INSERT OR IGNORE INTO marcas (nome) SELECT nome FROM marcas_div")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM marcas")
    print(f"✓ Marcas: {cursor.fetchone()[0]}")
except Exception as e:
    print(f"✗ Erro ao copiar marcas: {e}")

# Copiar categorias
try:
    cursor.execute("INSERT OR IGNORE INTO categorias (nome) SELECT nome FROM categorias_div")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM categorias")
    print(f"✓ Categorias: {cursor.fetchone()[0]}")
except Exception as e:
    print(f"✗ Erro ao copiar categorias: {e}")

conn.close()
print("\n✓ Dados copiados com sucesso!")

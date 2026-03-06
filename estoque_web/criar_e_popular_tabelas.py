import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estoque.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== CRIANDO E POPULANDO TABELAS ===\n")

# Criar tabela unidades
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(50) NOT NULL UNIQUE
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO unidades (nome) SELECT nome FROM unidades_div")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM unidades")
    print(f"✓ Unidades: {cursor.fetchone()[0]}")
except Exception as e:
    print(f"✗ Erro ao criar/popular unidades: {e}")

# Criar tabela marcas
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marcas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL UNIQUE
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO marcas (nome) SELECT nome FROM marcas_div")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM marcas")
    print(f"✓ Marcas: {cursor.fetchone()[0]}")
except Exception as e:
    print(f"✗ Erro ao criar/popular marcas: {e}")

# Criar tabela categorias
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL UNIQUE
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO categorias (nome) SELECT nome FROM categorias_div")
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM categorias")
    print(f"✓ Categorias: {cursor.fetchone()[0]}")
except Exception as e:
    print(f"✗ Erro ao criar/popular categorias: {e}")

conn.close()
print("\n✓ Tabelas criadas e populadas com sucesso!")

import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estoque.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== ADICIONANDO COLUNA CELULAR ===\n")

try:
    # Verificar se a coluna já existe
    cursor.execute("PRAGMA table_info(funcionarios)")
    colunas = [col[1] for col in cursor.fetchall()]
    
    if 'celular' not in colunas:
        # Adicionar coluna celular
        cursor.execute("ALTER TABLE funcionarios ADD COLUMN celular VARCHAR(20)")
        conn.commit()
        print("✓ Coluna 'celular' adicionada com sucesso!")
    else:
        print("✓ Coluna 'celular' já existe!")
        
except Exception as e:
    print(f"✗ Erro: {e}")

conn.close()

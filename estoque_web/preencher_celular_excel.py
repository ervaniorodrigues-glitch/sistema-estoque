import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'estoque.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== PREENCHENDO CELULAR A PARTIR DO TELEFONE ===\n")

# Se celular está vazio, copiar do telefone
cursor.execute("""
    UPDATE funcionarios 
    SET celular = telefone 
    WHERE celular IS NULL OR celular = ''
""")

conn.commit()
print(f"✓ {cursor.rowcount} funcionários atualizados!")

# Verificar resultado
cursor.execute("SELECT id, nome, telefone, celular FROM funcionarios LIMIT 5")
print("\nResultado:")
for row in cursor.fetchall():
    print(f"  {row[1]}: Tel={row[2]}, Cel={row[3]}")

conn.close()

import sqlite3

conn = sqlite3.connect('estoque_web.db')
cursor = conn.cursor()

# Buscar duplicados
cursor.execute('''
    SELECT cpfcnpj, COUNT(*) as total
    FROM clientes
    WHERE cpfcnpj IS NOT NULL AND cpfcnpj != ''
    GROUP BY cpfcnpj
    HAVING COUNT(*) > 1
''')

duplicados = cursor.fetchall()

print(f"Encontrados {len(duplicados)} CPF/CNPJ duplicados:")
for cpfcnpj, total in duplicados:
    print(f"  - {cpfcnpj}: {total} registros")
    
    # Buscar todos os registros com esse CPF/CNPJ
    cursor.execute('SELECT id, nome FROM clientes WHERE cpfcnpj = ? ORDER BY id', (cpfcnpj,))
    registros = cursor.fetchall()
    
    # Manter apenas o primeiro, deletar os outros
    for i, (id_cliente, nome) in enumerate(registros):
        if i == 0:
            print(f"    ✓ Mantendo: ID {id_cliente} - {nome}")
        else:
            print(f"    ✗ Removendo: ID {id_cliente} - {nome}")
            cursor.execute('DELETE FROM clientes WHERE id = ?', (id_cliente,))

conn.commit()
conn.close()

print("\n✅ Duplicados removidos com sucesso!")

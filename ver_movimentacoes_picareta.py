import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

print('=' * 80)
print('TODAS AS MOVIMENTAÇÕES DA PICARETA (Código 2)')
print('=' * 80)
print()

cursor.execute('''
    SELECT id, codigo_produto, tipo_movimento, quantidade_movimento, origem, data_movimento 
    FROM log_movimentacoes 
    WHERE codigo_produto = "2" 
    ORDER BY id
''')

movimentacoes = cursor.fetchall()

total_entradas = 0
total_saidas = 0

for mov in movimentacoes:
    id_mov, cod_prod, tipo, qtd, origem, data = mov
    print(f'ID: {id_mov} | Tipo: {tipo} | Qtd: {qtd} | Origem: {origem} | Data: {data}')
    
    if tipo in ('E', 'ENTRADA'):
        if qtd:
            total_entradas += qtd
    elif tipo in ('S', 'SAIDA'):
        if qtd:
            total_saidas += qtd

print()
print('=' * 80)
print(f'TOTAL ENTRADAS: {total_entradas}')
print(f'TOTAL SAÍDAS: {total_saidas}')
print(f'SALDO: {total_entradas - total_saidas}')
print('=' * 80)

conn.close()

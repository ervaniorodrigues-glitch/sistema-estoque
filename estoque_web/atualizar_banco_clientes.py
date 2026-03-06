"""
Script para atualizar o banco de dados - Remover coluna fax e adicionar unique constraint no CPF/CNPJ
"""
import sqlite3
import os

# Caminho do banco de dados
db_path = 'estoque_web.db'

if not os.path.exists(db_path):
    print(f"Banco de dados {db_path} não encontrado!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("Iniciando atualização do banco de dados...")
    
    # 1. Criar tabela temporária sem a coluna fax e com unique constraint
    print("1. Criando tabela temporária...")
    cursor.execute('''
        CREATE TABLE clientes_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(200) NOT NULL,
            email VARCHAR(100),
            cpfcnpj VARCHAR(18) UNIQUE,
            telefone VARCHAR(20),
            celular VARCHAR(20),
            endereco VARCHAR(200),
            cidade VARCHAR(100),
            uf VARCHAR(2),
            cep VARCHAR(10),
            anotacoes TEXT,
            ativo BOOLEAN DEFAULT 1,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Copiar dados da tabela antiga para a nova (sem a coluna fax)
    print("2. Copiando dados...")
    cursor.execute('''
        INSERT INTO clientes_new (id, nome, email, cpfcnpj, telefone, celular, endereco, cidade, uf, cep, anotacoes, ativo, data_cadastro)
        SELECT id, nome, email, cpfcnpj, telefone, celular, endereco, cidade, uf, cep, anotacoes, ativo, data_cadastro
        FROM clientes
    ''')
    
    # 3. Remover tabela antiga
    print("3. Removendo tabela antiga...")
    cursor.execute('DROP TABLE clientes')
    
    # 4. Renomear tabela nova
    print("4. Renomeando tabela nova...")
    cursor.execute('ALTER TABLE clientes_new RENAME TO clientes')
    
    # Commit das alterações
    conn.commit()
    print("\n✅ Banco de dados atualizado com sucesso!")
    print("   - Coluna 'fax' removida")
    print("   - Constraint UNIQUE adicionada ao CPF/CNPJ")
    
except Exception as e:
    conn.rollback()
    print(f"\n❌ Erro ao atualizar banco de dados: {e}")
    
finally:
    conn.close()

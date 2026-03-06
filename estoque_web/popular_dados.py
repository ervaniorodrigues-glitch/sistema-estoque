#!/usr/bin/env python
"""Script para popular o banco com dados de teste"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Fornecedor, Funcionario

with app.app_context():
    # Limpar dados antigos
    Fornecedor.query.delete()
    Funcionario.query.delete()
    db.session.commit()
    print("✓ Dados antigos removidos")
    
    # Adicionar fornecedores
    fornecedores = [
        Fornecedor(nome='Megabras Ind Eletrônica', telefone='(11) 5641-8111', celular='(11) 98765-4321', 
                   email='contato@megabras.com.br', oficina='Eletrônicos', endereco='Rua Gibraltar, 172',
                   cidade='São Paulo', uf='SP', cep='01310-100', cnpj='12.345.678/0001-90', contato='João Silva'),
        Fornecedor(nome='Distribuidora ABC', telefone='(21) 3333-4444', celular='(21) 99999-8888',
                   email='vendas@abc.com.br', oficina='Geral', endereco='Av. Brasil, 500',
                   cidade='Rio de Janeiro', uf='RJ', cep='20000-000', cnpj='98.765.432/0001-10', contato='Maria Santos'),
        Fornecedor(nome='Fornecedor XYZ', telefone='(31) 2222-3333', celular='(31) 97777-6666',
                   email='info@xyz.com.br', oficina='Peças', endereco='Rua das Flores, 100',
                   cidade='Belo Horizonte', uf='MG', cep='30000-000', cnpj='11.111.111/0001-11', contato='Pedro Costa'),
    ]
    
    for f in fornecedores:
        db.session.add(f)
    
    db.session.commit()
    print(f"✓ {len(fornecedores)} fornecedores adicionados")
    
    # Adicionar funcionários
    from datetime import date
    funcionarios = [
        Funcionario(nome='João da Silva', cargo='Gerente', cpf='123.456.789-00',
                    email='joao@empresa.com', telefone='(11) 98765-4321',
                    endereco='Rua A, 123', cidade='São Paulo', uf='SP', cep='01310-100',
                    data_admissao=date(2020, 1, 15), salario=5000.00, ativo=True),
        Funcionario(nome='Maria Santos', cargo='Vendedora', cpf='987.654.321-00',
                    email='maria@empresa.com', telefone='(11) 99999-8888',
                    endereco='Rua B, 456', cidade='São Paulo', uf='SP', cep='01310-200',
                    data_admissao=date(2021, 3, 20), salario=3000.00, ativo=True),
        Funcionario(nome='Pedro Costa', cargo='Operador', cpf='456.789.123-00',
                    email='pedro@empresa.com', telefone='(11) 97777-6666',
                    endereco='Rua C, 789', cidade='São Paulo', uf='SP', cep='01310-300',
                    data_admissao=date(2022, 6, 10), salario=2500.00, ativo=True),
    ]
    
    for f in funcionarios:
        db.session.add(f)
    
    db.session.commit()
    print(f"✓ {len(funcionarios)} funcionários adicionados")
    
    print("\n✓ Banco populado com sucesso!")

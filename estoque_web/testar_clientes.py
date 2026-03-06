import requests
import json

base_url = "http://127.0.0.1:5000"

# Teste 1: Criar cliente com CPF
print("Teste 1: Criar primeiro cliente com CPF 111.111.111-11")
response = requests.post(f"{base_url}/api/clientes", json={
    "nome": "Cliente Teste 1",
    "cpfcnpj": "111.111.111-11",
    "telefone": "(11) 1111-1111",
    "celular": "(11) 1-1111-1111"
})
print(f"Status: {response.status_code}")
print(f"Resposta: {response.json()}\n")

# Teste 2: Tentar criar outro cliente com o MESMO CPF
print("Teste 2: Tentar criar segundo cliente com MESMO CPF 111.111.111-11")
response = requests.post(f"{base_url}/api/clientes", json={
    "nome": "Cliente Teste 2 (DUPLICADO)",
    "cpfcnpj": "111.111.111-11",
    "telefone": "(22) 2222-2222"
})
print(f"Status: {response.status_code}")
print(f"Resposta: {response.json()}\n")

# Teste 3: Listar clientes
print("Teste 3: Listar todos os clientes")
response = requests.get(f"{base_url}/api/clientes?busca=&ativo=todos")
clientes = response.json()
print(f"Total de clientes: {len(clientes)}")
for c in clientes:
    print(f"  - {c['nome']} - CPF/CNPJ: {c['cpfcnpj']}")

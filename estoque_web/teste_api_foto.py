import requests
import json

# Testar a API
response = requests.get('http://127.0.0.1:5000/api/produtos?busca=colher')
produtos = response.json()

print("Resposta da API:")
print(json.dumps(produtos, indent=2, ensure_ascii=False))

if produtos:
    p = produtos[0]
    print(f"\n=== PRODUTO ===")
    print(f"Código: {p['codigo']}")
    print(f"Descrição: {p['descricao']}")
    print(f"Foto: {p.get('foto')}")
    print(f"Tipo da foto: {type(p.get('foto'))}")
    print(f"Foto é None?: {p.get('foto') is None}")
    print(f"Foto é vazia?: {p.get('foto') == ''}")

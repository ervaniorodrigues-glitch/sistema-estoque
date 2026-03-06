import sys
sys.path.insert(0, 'estoque_web')
from app import app
import json

with app.app_context():
    with app.test_client() as client:
        response = client.get('/api/movimentacoes')
        data = response.get_json()
        for item in data[:5]:
            print(f"ID: {item['id']}, Nota: {item['nota_fiscal']}, Obs: {item.get('observacao', 'CAMPO NÃO EXISTE')}")

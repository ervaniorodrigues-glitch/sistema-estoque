import sys
sys.path.insert(0, '.')
from app import app, Produto

with app.app_context():
    produtos = Produto.query.limit(5).all()
    print(f"Total de produtos: {Produto.query.count()}")
    print("\nPrimeiros 5 produtos:")
    for p in produtos:
        print(f"ID: {p.codigo} | Descrição: {p.descricao} | Foto: {p.foto}")

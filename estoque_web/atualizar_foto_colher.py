import sys
sys.path.insert(0, '.')
from app import app, Produto, db

with app.app_context():
    # Buscar o produto colher de pedreiro
    produto = Produto.query.filter_by(codigo=1).first()
    
    if produto:
        print(f"Produto encontrado: {produto.descricao}")
        print(f"Foto atual: {produto.foto}")
        
        produto.foto = 'colher-de-pedreiro.jpg'
        db.session.commit()
        
        print(f"Foto atualizada para: {produto.foto}")
        print("Sucesso!")
    else:
        print("Produto não encontrado!")

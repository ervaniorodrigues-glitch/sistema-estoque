import sys
sys.path.insert(0, '.')
from app import app, Produto, db

with app.app_context():
    # Buscar o produto
    produto = Produto.query.filter_by(codigo=1).first()
    
    print("=== ANTES DA ALTERAÇÃO ===")
    print(f"Código: {produto.codigo}")
    print(f"Descrição: {produto.descricao}")
    print(f"Foto: {produto.foto}")
    
    # Alterar a foto
    produto.foto = 'sdsdsds.jpg'
    db.session.commit()
    
    print("\n=== DEPOIS DA ALTERAÇÃO ===")
    produto = Produto.query.filter_by(codigo=1).first()
    print(f"Código: {produto.codigo}")
    print(f"Descrição: {produto.descricao}")
    print(f"Foto: {produto.foto}")

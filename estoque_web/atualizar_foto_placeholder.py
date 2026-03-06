import sys
sys.path.insert(0, '.')
from app import app, Produto, db

with app.app_context():
    # Atualizar todos os produtos que têm placeholder.svg
    produtos = Produto.query.filter_by(foto='placeholder.svg').all()
    
    print(f"Encontrados {len(produtos)} produtos com placeholder.svg")
    
    for p in produtos:
        p.foto = 'placeholder.jpg'
        print(f"Atualizado produto {p.codigo}: {p.descricao}")
    
    db.session.commit()
    print("\nAtualização concluída!")

import sys
sys.path.insert(0, 'estoque_web')
from app import app, db, Movimentacao

with app.app_context():
    movs = Movimentacao.query.limit(10).all()
    for m in movs:
        print(f'ID: {m.id}, Nota: {m.nota_fiscal}, Obs: "{m.observacao}"')

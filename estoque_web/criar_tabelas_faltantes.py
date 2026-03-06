from app import app, db

with app.app_context():
    # Criar todas as tabelas que faltam
    db.create_all()
    print("✓ Tabelas criadas com sucesso!")

from app import app, db

with app.app_context():
    print("Criando todas as tabelas...")
    db.create_all()
    print("✅ Tabelas criadas com sucesso!")

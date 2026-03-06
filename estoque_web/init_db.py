"""
Script para inicializar o banco de dados SQLite
"""

from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Criar todas as tabelas
        print("Criando tabelas...")
        db.create_all()
        
        # Criar usuário admin padrão
        admin = Usuario.query.filter_by(usuario='admin').first()
        if not admin:
            admin = Usuario(
                nome='Administrador',
                usuario='admin',
                senha=generate_password_hash('admin123'),
                admin=True,
                ativo=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado (usuário: admin, senha: admin123)")
        else:
            print("✅ Usuário admin já existe")
        
        print("✅ Banco de dados inicializado com sucesso!")
        print("\nPara iniciar o sistema:")
        print("  python app.py")
        print("\nAcesse: http://localhost:5000")
        print("Login: admin / admin123")

if __name__ == '__main__':
    init_database()

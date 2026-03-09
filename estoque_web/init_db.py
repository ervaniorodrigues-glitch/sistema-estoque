"""
Script para inicializar o banco de dados e criar usuário master
Execute este script após o primeiro deploy
"""

from app import app, db, Usuario
from werkzeug.security import generate_password_hash
import os

def init_database():
    """Inicializa o banco de dados e cria usuário master"""
    with app.app_context():
        # Criar todas as tabelas
        print("Criando tabelas do banco de dados...")
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar se já existe usuário master
        master = Usuario.query.filter_by(usuario='master').first()
        
        if not master:
            print("\n📝 Criando usuário master...")
            senha_master = os.environ.get('MASTER_PASSWORD', '@Senha01')
            
            master = Usuario(
                usuario='master',
                senha=generate_password_hash(senha_master),
                nome='Administrador',
                admin=True,
                tipo='master',
                ativo=True
            )
            
            db.session.add(master)
            db.session.commit()
            
            print("✅ Usuário master criado com sucesso!")
            print("\n" + "="*50)
            print("CREDENCIAIS DE ACESSO:")
            print(f"Usuário: master")
            print(f"Senha: {senha_master}")
            print("="*50)
            print("\n⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        else:
            print("✅ Usuário master já existe!")
        
        print("\n🎉 Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    init_database()

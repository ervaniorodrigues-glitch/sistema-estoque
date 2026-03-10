"""
Script para inicializar banco de dados no Render via URL
"""
import os
import sys

# Adicionar o diretório estoque_web ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'estoque_web'))

from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def init_database():
    """Inicializa o banco de dados"""
    with app.app_context():
        print("🔧 Criando tabelas...")
        db.create_all()
        print("✅ Tabelas criadas!")
        
        # Verificar se usuário master já existe
        master = Usuario.query.filter_by(usuario='master').first()
        
        if not master:
            print("👤 Criando usuário master...")
            master = Usuario(
                nome='Administrador Master',
                usuario='master',
                senha=generate_password_hash('@Senha01'),
                admin=True,
                tipo='admin',
                ativo=True
            )
            db.session.add(master)
            db.session.commit()
            print("✅ Usuário master criado!")
            print("   Usuário: master")
            print("   Senha: @Senha01")
        else:
            print("✅ Usuário master já existe!")
        
        print("\n🎉 Banco de dados inicializado com sucesso!")
        return True

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

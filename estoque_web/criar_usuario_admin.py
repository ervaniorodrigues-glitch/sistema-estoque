#!/usr/bin/env python
"""Criar usuário admin padrão"""
import os
from werkzeug.security import generate_password_hash
from app import app, db, Usuario

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with app.app_context():
    # Verificar se já existe usuário admin
    admin = Usuario.query.filter_by(usuario='admin').first()
    
    if admin:
        print("✓ Usuário admin já existe!")
    else:
        # Criar usuário admin
        usuario_admin = Usuario(
            nome='Administrador',
            usuario='admin',
            senha=generate_password_hash('admin'),
            admin=True,
            ativo=True
        )
        
        db.session.add(usuario_admin)
        db.session.commit()
        
        print("✓ Usuário admin criado com sucesso!")
        print("  Usuário: admin")
        print("  Senha: admin")

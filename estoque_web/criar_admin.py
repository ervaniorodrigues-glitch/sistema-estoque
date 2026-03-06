#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Criar usuário admin"""

from app import app, db, Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    # Verificar se admin já existe
    admin = Usuario.query.filter_by(usuario='admin').first()
    
    if admin:
        # Atualizar senha
        admin.senha = generate_password_hash('admin')
        db.session.commit()
        print("✅ Senha do admin atualizada para: admin")
    else:
        # Criar novo admin
        admin = Usuario(
            nome='Administrador',
            usuario='admin',
            senha=generate_password_hash('admin'),
            admin=True,
            ativo=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuário admin criado com sucesso!")
        print("   Usuário: admin")
        print("   Senha: admin")

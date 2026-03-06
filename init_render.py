#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para inicializar o banco de dados no Render
"""

import os
import sys

# Adicionar o diretório estoque_web ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'estoque_web'))

from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def init_database():
    """Inicializa o banco de dados com tabelas e usuário admin"""
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        print("✓ Tabelas criadas com sucesso!")
        
        # Verificar se já existe usuário admin
        admin = Usuario.query.filter_by(usuario='admin').first()
        
        if not admin:
            # Criar usuário admin padrão
            admin = Usuario(
                nome='Administrador',
                usuario='admin',
                senha=generate_password_hash('admin123'),
                admin=True,
                ativo=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Usuário admin criado!")
            print("  Usuário: admin")
            print("  Senha: admin123")
        else:
            print("✓ Usuário admin já existe!")

if __name__ == '__main__':
    init_database()

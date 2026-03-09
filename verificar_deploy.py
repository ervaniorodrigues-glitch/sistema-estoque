#!/usr/bin/env python3
"""
Script de verificação pré-deploy
Verifica se todos os arquivos necessários estão presentes e configurados corretamente
"""

import os
import sys

def verificar_arquivo(caminho, descricao):
    """Verifica se um arquivo existe"""
    if os.path.exists(caminho):
        print(f"✅ {descricao}: {caminho}")
        return True
    else:
        print(f"❌ {descricao} NÃO ENCONTRADO: {caminho}")
        return False

def verificar_conteudo(caminho, texto, descricao):
    """Verifica se um arquivo contém determinado texto"""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            if texto in conteudo:
                print(f"✅ {descricao}")
                return True
            else:
                print(f"⚠️  {descricao} - NÃO ENCONTRADO")
                return False
    except:
        print(f"❌ Erro ao ler {caminho}")
        return False

def main():
    print("=" * 60)
    print("🔍 VERIFICAÇÃO PRÉ-DEPLOY - SISTEMA DE ESTOQUE")
    print("=" * 60)
    print()
    
    erros = 0
    avisos = 0
    
    # Verificar estrutura de diretórios
    print("📁 Verificando estrutura de diretórios...")
    if not verificar_arquivo("estoque_web", "Diretório principal"):
        erros += 1
    if not verificar_arquivo("estoque_web/templates", "Diretório de templates"):
        erros += 1
    if not verificar_arquivo("estoque_web/static", "Diretório de arquivos estáticos"):
        erros += 1
    print()
    
    # Verificar arquivos essenciais
    print("📄 Verificando arquivos essenciais...")
    if not verificar_arquivo("estoque_web/app.py", "Aplicação principal"):
        erros += 1
    if not verificar_arquivo("estoque_web/requirements.txt", "Dependências Python"):
        erros += 1
    if not verificar_arquivo("estoque_web/render.yaml", "Configuração do Render"):
        erros += 1
    if not verificar_arquivo("estoque_web/init_db.py", "Script de inicialização do banco"):
        erros += 1
    if not verificar_arquivo("estoque_web/.env.example", "Exemplo de variáveis de ambiente"):
        erros += 1
    print()
    
    # Verificar configurações no app.py
    print("⚙️  Verificando configurações no app.py...")
    if not verificar_conteudo("estoque_web/app.py", "os.getenv('SECRET_KEY')", "SECRET_KEY via variável de ambiente"):
        erros += 1
    if not verificar_conteudo("estoque_web/app.py", "os.getenv('DATABASE_URL')", "DATABASE_URL via variável de ambiente"):
        erros += 1
    if not verificar_conteudo("estoque_web/app.py", "postgresql://", "Suporte a PostgreSQL"):
        erros += 1
    print()
    
    # Verificar dependências
    print("📦 Verificando dependências no requirements.txt...")
    if not verificar_conteudo("estoque_web/requirements.txt", "Flask", "Flask"):
        erros += 1
    if not verificar_conteudo("estoque_web/requirements.txt", "gunicorn", "Gunicorn (servidor WSGI)"):
        erros += 1
    if not verificar_conteudo("estoque_web/requirements.txt", "psycopg2-binary", "psycopg2-binary (PostgreSQL)"):
        erros += 1
    if not verificar_conteudo("estoque_web/requirements.txt", "Flask-SQLAlchemy", "Flask-SQLAlchemy"):
        erros += 1
    print()
    
    # Verificar render.yaml
    print("🔧 Verificando render.yaml...")
    if not verificar_conteudo("estoque_web/render.yaml", "gunicorn app:app", "Comando de start correto"):
        erros += 1
    if not verificar_conteudo("estoque_web/render.yaml", "pip install -r requirements.txt", "Comando de build correto"):
        erros += 1
    if not verificar_conteudo("estoque_web/render.yaml", "SECRET_KEY", "Configuração de SECRET_KEY"):
        erros += 1
    if not verificar_conteudo("estoque_web/render.yaml", "DATABASE_URL", "Configuração de DATABASE_URL"):
        erros += 1
    print()
    
    # Verificar se há arquivos sensíveis
    print("🔒 Verificando segurança...")
    if os.path.exists("estoque_web/.env"):
        print("⚠️  Arquivo .env encontrado - NÃO COMMITE ESTE ARQUIVO!")
        avisos += 1
    else:
        print("✅ Arquivo .env não encontrado (correto)")
    
    if os.path.exists("estoque_web/instance/estoque.db"):
        print("⚠️  Banco SQLite local encontrado - será ignorado em produção")
        avisos += 1
    print()
    
    # Verificar .gitignore
    print("📝 Verificando .gitignore...")
    if os.path.exists(".gitignore"):
        if verificar_conteudo(".gitignore", ".env", ".env no .gitignore"):
            pass
        else:
            print("⚠️  Adicione .env ao .gitignore!")
            avisos += 1
        if verificar_conteudo(".gitignore", "*.db", "*.db no .gitignore"):
            pass
        else:
            print("⚠️  Adicione *.db ao .gitignore!")
            avisos += 1
    else:
        print("⚠️  Arquivo .gitignore não encontrado")
        avisos += 1
    print()
    
    # Resumo
    print("=" * 60)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("=" * 60)
    if erros == 0 and avisos == 0:
        print("✅ Sistema pronto para deploy!")
        print()
        print("Próximos passos:")
        print("1. Commit e push do código para o repositório")
        print("2. Criar conta no Render (https://render.com)")
        print("3. Seguir o guia em estoque_web/DEPLOY_RENDER.md")
        return 0
    else:
        if erros > 0:
            print(f"❌ {erros} erro(s) encontrado(s) - CORRIJA ANTES DO DEPLOY")
        if avisos > 0:
            print(f"⚠️  {avisos} aviso(s) encontrado(s) - REVISE ANTES DO DEPLOY")
        print()
        print("Corrija os problemas acima antes de fazer o deploy.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

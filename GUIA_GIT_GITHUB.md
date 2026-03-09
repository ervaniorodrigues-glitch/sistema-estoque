# 📘 Guia Completo: Git e GitHub

## ✅ Git já está instalado!

Versão detectada: **Git 2.53.0**

## 🔧 Passo 1: Configurar Git (FAÇA ISSO PRIMEIRO)

Abra o PowerShell ou Git Bash e execute:

```bash
# Configure seu nome (use seu nome real)
git config --global user.name "Seu Nome Aqui"

# Configure seu email (use o email que vai usar no GitHub)
git config --global user.email "seu.email@exemplo.com"

# Verificar configurações
git config --global user.name
git config --global user.email
```

**Exemplo:**
```bash
git config --global user.name "Ervanio Rodrigues"
git config --global user.email "ervanio@exemplo.com"
```

## 🌐 Passo 2: Criar Conta no GitHub

1. Acesse: https://github.com
2. Clique em "Sign up"
3. Preencha:
   - Username (nome de usuário único)
   - Email (o mesmo que configurou no Git)
   - Password (senha forte)
4. Verifique seu email
5. Complete o perfil

## 📦 Passo 3: Criar Repositório no GitHub

### Opção A: Via Interface Web (Recomendado)

1. Faça login no GitHub
2. Clique no "+" no canto superior direito
3. Selecione "New repository"
4. Configure:
   - **Repository name**: `sistema-estoque` (ou outro nome)
   - **Description**: "Sistema de Gestão de Estoque com Flask"
   - **Visibility**: Private (recomendado) ou Public
   - **NÃO** marque "Initialize with README"
   - **NÃO** adicione .gitignore ou license ainda
5. Clique em "Create repository"
6. **COPIE** a URL que aparece (ex: `https://github.com/seu-usuario/sistema-estoque.git`)

## 🚀 Passo 4: Inicializar Git no Projeto

No PowerShell, dentro da pasta do projeto, execute:

```bash
# 1. Inicializar repositório Git
git init

# 2. Adicionar todos os arquivos
git add .

# 3. Fazer o primeiro commit
git commit -m "Primeiro commit - Sistema de Estoque v2.0"

# 4. Renomear branch para main (se necessário)
git branch -M main

# 5. Adicionar o repositório remoto (SUBSTITUA pela sua URL)
git remote add origin https://github.com/SEU-USUARIO/sistema-estoque.git

# 6. Enviar para o GitHub
git push -u origin main
```

### ⚠️ Se pedir autenticação:

O GitHub não aceita mais senha via HTTPS. Você precisa usar um **Personal Access Token (PAT)**.

#### Como criar um Token:

1. No GitHub, clique na sua foto (canto superior direito)
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. "Generate new token" → "Generate new token (classic)"
4. Configure:
   - **Note**: "Token para Sistema de Estoque"
   - **Expiration**: 90 days (ou No expiration)
   - **Scopes**: Marque "repo" (acesso completo aos repositórios)
5. Clique em "Generate token"
6. **COPIE O TOKEN** (você não verá ele novamente!)

#### Usar o Token:

Quando o Git pedir senha, use o **token** no lugar da senha:
- Username: seu-usuario-github
- Password: cole-o-token-aqui

## 📝 Comandos Git Úteis

```bash
# Ver status dos arquivos
git status

# Ver histórico de commits
git log --oneline

# Adicionar arquivos específicos
git add arquivo.py

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para o GitHub
git push

# Baixar mudanças do GitHub
git pull

# Ver repositórios remotos
git remote -v

# Criar nova branch
git checkout -b nome-da-branch

# Voltar para main
git checkout main
```

## 🔄 Workflow Diário

Depois do setup inicial, para atualizar o código:

```bash
# 1. Ver o que mudou
git status

# 2. Adicionar mudanças
git add .

# 3. Fazer commit
git commit -m "Descrição do que foi alterado"

# 4. Enviar para GitHub
git push
```

## 🐛 Problemas Comuns

### Erro: "fatal: not a git repository"
**Solução**: Execute `git init` na pasta do projeto

### Erro: "failed to push some refs"
**Solução**: Execute `git pull origin main` antes de fazer push

### Erro: "Authentication failed"
**Solução**: Use Personal Access Token ao invés de senha

### Erro: "remote origin already exists"
**Solução**: 
```bash
git remote remove origin
git remote add origin https://github.com/seu-usuario/repo.git
```

## 📋 Checklist Completo

- [ ] Git instalado (✅ JÁ ESTÁ!)
- [ ] Configurar nome: `git config --global user.name "Seu Nome"`
- [ ] Configurar email: `git config --global user.email "seu@email.com"`
- [ ] Criar conta no GitHub
- [ ] Criar repositório no GitHub
- [ ] Copiar URL do repositório
- [ ] Executar `git init` na pasta do projeto
- [ ] Executar `git add .`
- [ ] Executar `git commit -m "Primeiro commit"`
- [ ] Executar `git remote add origin URL`
- [ ] Executar `git push -u origin main`
- [ ] Criar Personal Access Token (se necessário)
- [ ] Verificar no GitHub se os arquivos foram enviados

## 🎯 Próximo Passo: Deploy no Render

Depois de enviar para o GitHub, siga o guia em `estoque_web/DEPLOY_RENDER.md`

## 📞 Recursos Úteis

- **Documentação Git**: https://git-scm.com/doc
- **GitHub Docs**: https://docs.github.com
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Aprender Git**: https://learngitbranching.js.org

---

**Dica**: Salve seu Personal Access Token em um lugar seguro (gerenciador de senhas)!

**Importante**: Nunca commite arquivos com senhas ou chaves secretas. O `.gitignore` já está configurado para ignorar `.env` e `*.db`.

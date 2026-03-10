# 🚀 Deploy no Render - Passo a Passo

## ✅ Pré-requisitos

1. Conta no GitHub (https://github.com)
2. Conta no Render (https://render.com)
3. Git instalado no seu computador

---

## 📋 PASSO 1: Preparar o Projeto

### 1.1 Verificar arquivos necessários

Seu projeto precisa ter:
- ✅ `requirements.txt` - Dependências Python
- ✅ `render.yaml` - Configuração do Render
- ✅ `.gitignore` - Arquivos a ignorar
- ✅ `estoque_web/app.py` - Aplicação principal

### 1.2 Criar arquivo `.gitignore` (se não existir)

```
instance/
*.db
__pycache__/
*.pyc
.env
venv/
.vscode/
Backup/
Backup_*/
*.zip
temp_*/
```

---

## 📋 PASSO 2: Subir para o GitHub

### 2.1 Inicializar Git (se ainda não fez)

```bash
git init
git add .
git commit -m "Deploy inicial - Sistema de Estoque"
```

### 2.2 Criar repositório no GitHub

1. Acesse: https://github.com/new
2. Nome do repositório: `sistema-estoque`
3. Deixe como **Público**
4. NÃO marque "Initialize with README"
5. Clique em "Create repository"

### 2.3 Conectar e enviar código

```bash
git remote add origin https://github.com/SEU_USUARIO/sistema-estoque.git
git branch -M main
git push -u origin main
```

---

## 📋 PASSO 3: Configurar PostgreSQL no Render

### 3.1 Criar banco PostgreSQL

1. Acesse: https://dashboard.render.com
2. Clique em "New +" → "PostgreSQL"
3. Preencha:
   - **Name**: `estoque-db`
   - **Database**: `estoque`
   - **User**: `estoque_user`
   - **Region**: `Oregon (US West)`
   - **Plan**: `Free`
4. Clique em "Create Database"
5. **IMPORTANTE**: Copie a "Internal Database URL" (começa com `postgresql://`)

---

## 📋 PASSO 4: Criar Web Service no Render

### 4.1 Criar serviço

1. No Render, clique em "New +" → "Web Service"
2. Conecte seu repositório GitHub
3. Selecione o repositório `sistema-estoque`
4. Preencha:
   - **Name**: `sistema-estoque`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Root Directory**: (deixe vazio)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT estoque_web.app:app`

### 4.2 Configurar variáveis de ambiente

Na seção "Environment Variables", adicione:

```
DATABASE_URL = [Cole aqui a Internal Database URL do PostgreSQL]
SECRET_KEY = sua_chave_secreta_aqui_123456
FLASK_ENV = production
```

### 4.3 Finalizar

1. **Plan**: Selecione `Free`
2. Clique em "Create Web Service"
3. Aguarde o deploy (5-10 minutos)

---

## 📋 PASSO 5: Inicializar Banco de Dados

### 5.1 Acessar Shell do Render

1. No painel do seu Web Service
2. Clique em "Shell" (no menu lateral)
3. Execute:

```bash
python estoque_web/init_db.py
```

---

## 📋 PASSO 6: Testar o Sistema

### 6.1 Acessar URL

Sua URL será algo como:
```
https://sistema-estoque.onrender.com
```

### 6.2 Fazer login

- **Usuário**: `master`
- **Senha**: `@Senha01`

### 6.3 Restaurar backup

1. Vá em "Sistema" → "Backup e Proteção"
2. Clique em "Restaurar Backup"
3. Selecione seu arquivo de backup
4. Aguarde a importação

---

## 🔧 Comandos Úteis

### Ver logs em tempo real
```bash
# No painel do Render, clique em "Logs"
```

### Forçar novo deploy
```bash
git add .
git commit -m "Atualização"
git push
```

### Reiniciar serviço
```bash
# No painel do Render, clique em "Manual Deploy" → "Clear build cache & deploy"
```

---

## ⚠️ Problemas Comuns

### 1. Erro "Application failed to start"
- Verifique os logs
- Confirme que `gunicorn` está no `requirements.txt`
- Verifique o comando de start

### 2. Erro de conexão com banco
- Verifique se a variável `DATABASE_URL` está correta
- Confirme que o PostgreSQL está rodando

### 3. Sistema hiberna após 15 minutos
- É normal no plano Free
- Use UptimeRobot para manter acordado (veja GUIA_RENDER_DEFINITIVO.md)

---

## 📞 Precisa de Ajuda?

Me avise em qual passo você está e qual erro apareceu!

---

**URL do Sistema**: https://sistema-estoque.onrender.com
**Usuário**: master
**Senha**: @Senha01

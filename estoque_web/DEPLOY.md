# 🚀 Guia de Deploy - Sistema de Controle de Estoque

## 📋 Pré-requisitos

- Conta no [Render](https://render.com) (gratuita)
- Conta no [GitHub](https://github.com) (gratuita)
- Git instalado localmente

---

## 🔧 Passo 1: Preparar o Código

### 1.1 Configurar variáveis de ambiente localmente (opcional)

Crie um arquivo `.env` na pasta `estoque_web/`:

```env
SECRET_KEY=sua_chave_secreta_super_segura_aqui
FLASK_ENV=development
SESSION_COOKIE_SECURE=False
```

### 1.2 Testar localmente

```bash
cd estoque_web
pip install -r requirements.txt
python init_db.py
python app.py
```

Acesse: http://127.0.0.1:5000

---

## 📦 Passo 2: Enviar para o GitHub

### 2.1 Criar repositório no GitHub

1. Acesse [GitHub](https://github.com) e faça login
2. Clique em "New repository"
3. Nome: `sistema-estoque` (ou outro nome)
4. Deixe como **Público** (necessário para plano gratuito do Render)
5. NÃO inicialize com README
6. Clique em "Create repository"

### 2.2 Enviar código

```bash
# Na pasta raiz do projeto
git init
git add .
git commit -m "Deploy inicial do sistema de estoque"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/sistema-estoque.git
git push -u origin main
```

**⚠️ Substitua `SEU_USUARIO` pelo seu usuário do GitHub!**

---

## 🌐 Passo 3: Deploy no Render

### 3.1 Criar conta no Render

1. Acesse [Render](https://render.com)
2. Faça login com sua conta do GitHub

### 3.2 Criar Web Service

1. No dashboard do Render, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub
4. Selecione o repositório `sistema-estoque`

### 3.3 Configurar o serviço

- **Name**: `sistema-estoque`
- **Region**: Oregon (US West)
- **Branch**: `main`
- **Root Directory**: `estoque_web`
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### 3.4 Configurar variáveis de ambiente

Adicione as seguintes variáveis de ambiente:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | (Clique em "Generate" para gerar automaticamente) |
| `FLASK_ENV` | `production` |
| `SESSION_COOKIE_SECURE` | `True` |
| `MASTER_PASSWORD` | `@Senha01` (ou outra senha segura) |

### 3.5 Criar banco de dados PostgreSQL

1. No dashboard do Render, clique em "New +"
2. Selecione "PostgreSQL"
3. **Name**: `estoque-db`
4. **Region**: Oregon (US West) - mesma região do web service
5. **Plan**: Free
6. Clique em "Create Database"

### 3.6 Conectar banco ao web service

1. Volte para o web service `sistema-estoque`
2. Vá em "Environment"
3. Adicione a variável:
   - **Key**: `DATABASE_URL`
   - **Value**: Copie a "Internal Database URL" do PostgreSQL criado

### 3.7 Inicializar o banco de dados

Após o primeiro deploy, execute o script de inicialização:

1. No dashboard do Render, vá no web service
2. Clique em "Shell" (no menu lateral)
3. Execute:
```bash
python init_db.py
```

---

## ✅ Passo 4: Acessar o Sistema

Após o deploy (leva 2-5 minutos), você receberá uma URL como:

```
https://sistema-estoque-xxxx.onrender.com
```

**Credenciais padrão:**
- Usuário: `master`
- Senha: `@Senha01` (ou a que você definiu em `MASTER_PASSWORD`)

---

## 🔄 Atualizar o Sistema

Quando fizer mudanças no código:

```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

O Render fará o deploy automaticamente!

---

## ⚠️ Importante - Plano Gratuito

O plano gratuito do Render tem algumas limitações:

1. **Sleep após inatividade**: O serviço "dorme" após 15 minutos sem uso
   - Primeira requisição após sleep demora ~30 segundos
   
2. **750 horas/mês**: Suficiente para uso pessoal/testes

3. **PostgreSQL**: 90 dias de retenção de dados no plano gratuito

---

## 🔒 Segurança

### Após o primeiro acesso:

1. ✅ Altere a senha do usuário master
2. ✅ Crie usuários intermediários conforme necessário
3. ✅ Não compartilhe a SECRET_KEY
4. ✅ Faça backups regulares do banco de dados

### Backup do banco de dados:

No Render, vá em PostgreSQL > Backups para configurar backups automáticos.

---

## 🆘 Problemas Comuns

### Deploy falhou?

1. Verifique os logs no painel do Render
2. Certifique-se que todos os arquivos foram enviados ao GitHub
3. Verifique se o `requirements.txt` está correto
4. Confirme que a `DATABASE_URL` está configurada

### Banco de dados não conecta?

1. Verifique se o PostgreSQL foi criado na mesma região
2. Confirme que a `DATABASE_URL` está correta
3. Execute `python init_db.py` no Shell do Render

### Sistema lento?

- Normal no plano gratuito após período de inatividade
- Considere upgrade para plano pago ($7/mês) para melhor performance

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs no Render
2. Consulte a [documentação do Render](https://render.com/docs)
3. Revise este guia passo a passo

---

## 🎉 Pronto!

Seu sistema de estoque está online e acessível de qualquer lugar!

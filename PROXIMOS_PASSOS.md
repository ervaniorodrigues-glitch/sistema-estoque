# 🎯 PRÓXIMOS PASSOS - DEPLOY NO RENDER

## ✅ O que já foi feito:

1. ✅ Sistema limpo e organizado
2. ✅ Código commitado no Git
3. ✅ Push para o GitHub em andamento...

## 🚀 Aguardando Push para o GitHub

O comando `git push` está enviando todos os arquivos para:
**https://github.com/ervaniorodrigues-glitch/sistema-estoque**

Isso pode levar alguns minutos dependendo da sua conexão.

### Se pedir autenticação:
- **Username**: ervaniorodrigues-glitch
- **Password**: Use um **Personal Access Token** (não a senha do GitHub)

#### Como criar o Token (se necessário):
1. GitHub → Settings (foto do perfil)
2. Developer settings → Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Marque: **repo** (acesso completo)
5. Generate token
6. **COPIE O TOKEN** e use como senha

---

## 📋 Após o Push Completar

### 1. Verificar no GitHub
- Acesse: https://github.com/ervaniorodrigues-glitch/sistema-estoque
- Confirme que todos os arquivos foram enviados
- Verifique se a pasta `estoque_web` está lá

### 2. Criar Conta no Render
- Acesse: https://render.com
- Clique em "Get Started"
- Faça login com GitHub (recomendado)
- Autorize o Render a acessar seus repositórios

### 3. Criar PostgreSQL Database no Render

1. No dashboard do Render, clique em **"New +"**
2. Selecione **"PostgreSQL"**
3. Configure:
   - **Name**: `estoque-db`
   - **Database**: `estoque`
   - **User**: `estoque_user`
   - **Region**: `Oregon (US West)`
   - **PostgreSQL Version**: 16
   - **Plan**: **Free**
4. Clique em **"Create Database"**
5. Aguarde a criação (1-2 minutos)
6. **IMPORTANTE**: Na página do banco, copie a **"Internal Database URL"**
   - Exemplo: `postgresql://estoque_user:senha@dpg-xxx/estoque`
   - **GUARDE ESSA URL** - você vai precisar dela!

### 4. Criar Web Service no Render

1. No dashboard, clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte ao repositório:
   - Selecione **"sistema-estoque"**
   - Clique em **"Connect"**
4. Configure:
   - **Name**: `sistema-estoque`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Root Directory**: `estoque_web`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: **Free**

### 5. Configurar Variáveis de Ambiente

Na seção **"Environment"**, adicione:

```
SECRET_KEY
  → Clique em "Generate" para criar automaticamente

DATABASE_URL
  → Cole a "Internal Database URL" do PostgreSQL que você copiou

FLASK_ENV
  → production

SESSION_COOKIE_SECURE
  → True

PYTHON_VERSION
  → 3.11.0
```

### 6. Deploy Automático

1. Clique em **"Create Web Service"**
2. O Render iniciará o deploy automaticamente
3. Aguarde 5-10 minutos
4. Acompanhe os logs na tela

### 7. Inicializar o Banco de Dados

Após o deploy completar:

1. Na página do Web Service, vá em **"Shell"** (menu lateral)
2. Execute o comando:
   ```bash
   python init_db.py
   ```
3. Aguarde a mensagem de sucesso
4. Digite `exit` para sair do shell

### 8. Acessar o Sistema

1. Na página do Web Service, copie a URL (ex: `https://sistema-estoque.onrender.com`)
2. Acesse no navegador
3. Faça login:
   - **Usuário**: `admin`
   - **Senha**: `admin123`
4. **IMPORTANTE**: Altere a senha do admin imediatamente!

---

## 🎉 Sistema Online!

Seu sistema estará disponível 24/7 na internet!

### ⚠️ Limitações do Plano Free:
- Hiberna após 15 minutos de inatividade
- Primeiro acesso pode levar 30-60 segundos
- 750 horas/mês de uso
- Uploads podem ser perdidos após redeploy

### 💰 Upgrade Recomendado (Opcional):
- **Starter Plan**: $7/mês - sem hibernação
- **PostgreSQL Starter**: $7/mês - com backups

---

## 📞 Precisa de Ajuda?

- **Guia completo**: `estoque_web/DEPLOY_RENDER.md`
- **Documentação Render**: https://render.com/docs
- **Status do Render**: https://status.render.com

---

## 🔄 Atualizações Futuras

Para atualizar o sistema depois:

```bash
# 1. Fazer alterações no código
# 2. Commit
git add .
git commit -m "Descrição das mudanças"

# 3. Push
git push

# 4. O Render fará deploy automático!
```

---

**Boa sorte com o deploy! 🚀**

Se tiver qualquer problema, consulte o guia completo em `estoque_web/DEPLOY_RENDER.md`

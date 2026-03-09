# 🚀 Deploy no PythonAnywhere - Guia Completo

## Por que PythonAnywhere?
- ✅ Suporte nativo a Flask e SQLite
- ✅ Disco persistente (seus dados não serão perdidos)
- ✅ Interface web simples
- ✅ 100% gratuito para projetos pequenos
- ✅ Sem necessidade de cartão de crédito

---

## 📋 Passo a Passo

### 1. Criar Conta no PythonAnywhere

1. Acesse: https://www.pythonanywhere.com
2. Clique em **"Start running Python online in less than a minute!"**
3. Clique em **"Create a Beginner account"**
4. Preencha:
   - Username (ex: ervaniorodrigues)
   - Email
   - Senha
5. Confirme o email

---

### 2. Fazer Upload do Código

#### Opção A: Via Git (Recomendado)

1. No dashboard do PythonAnywhere, clique em **"Consoles"**
2. Clique em **"Bash"** para abrir um terminal
3. No terminal, execute:

```bash
# Clonar seu repositório
git clone https://github.com/ervaniorodrigues-glitch/sistema-estoque.git

# Entrar na pasta
cd sistema-estoque/estoque_web

# Verificar se os arquivos estão lá
ls -la
```

#### Opção B: Via Upload Manual

1. Clique em **"Files"** no menu
2. Navegue até `/home/seu_usuario/`
3. Crie uma pasta: `sistema-estoque`
4. Faça upload dos arquivos da pasta `estoque_web`

---

### 3. Instalar Dependências

No console Bash do PythonAnywhere:

```bash
# Ir para a pasta do projeto
cd ~/sistema-estoque/estoque_web

# Criar ambiente virtual
python3.10 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

### 4. Configurar Web App

1. No dashboard, clique em **"Web"**
2. Clique em **"Add a new web app"**
3. Clique em **"Next"** (aceitar o domínio gratuito)
4. Selecione **"Manual configuration"**
5. Selecione **"Python 3.10"**
6. Clique em **"Next"**

---

### 5. Configurar WSGI

1. Na página Web, role até **"Code"**
2. Clique no link do arquivo **WSGI configuration file**
3. **Apague todo o conteúdo** e cole:

```python
import sys
import os

# Adicionar o diretório do projeto ao path
path = '/home/SEU_USUARIO/sistema-estoque/estoque_web'
if path not in sys.path:
    sys.path.append(path)

# Configurar variáveis de ambiente
os.environ['SECRET_KEY'] = 'sua-chave-secreta-aqui-mude-isso'

# Importar a aplicação Flask
from app import app as application
```

**IMPORTANTE**: Substitua `SEU_USUARIO` pelo seu username do PythonAnywhere!

4. Clique em **"Save"**

---

### 6. Configurar Virtualenv

1. Na página Web, role até **"Virtualenv"**
2. No campo **"Enter path to a virtualenv"**, digite:
   ```
   /home/SEU_USUARIO/sistema-estoque/estoque_web/venv
   ```
3. Clique no ícone de ✓ (check)

---

### 7. Configurar Arquivos Estáticos

1. Na página Web, role até **"Static files"**
2. Adicione:
   - **URL**: `/static/`
   - **Directory**: `/home/SEU_USUARIO/sistema-estoque/estoque_web/static`

---

### 8. Upload do Banco de Dados

#### Via Console Bash:

```bash
cd ~/sistema-estoque/estoque_web

# Se você clonou via Git, o banco já está lá
# Verificar se existe
ls -la instance/

# Se não existir, criar a pasta
mkdir -p instance

# Fazer upload do banco (use a interface Files)
```

#### Via Interface Files:

1. Clique em **"Files"**
2. Navegue até `/home/seu_usuario/sistema-estoque/estoque_web/instance/`
3. Clique em **"Upload a file"**
4. Selecione seu arquivo `estoque.db` local
5. Faça upload

---

### 9. Iniciar o Web App

1. Volte para a página **"Web"**
2. No topo, clique no botão verde **"Reload seu_usuario.pythonanywhere.com"**
3. Aguarde alguns segundos
4. Clique no link do seu site (ex: `ervaniorodrigues.pythonanywhere.com`)

---

### 10. Testar o Sistema

1. Acesse: `https://seu_usuario.pythonanywhere.com`
2. Faça login com:
   - Usuário: `master`
   - Senha: `@Senha01`
3. Verifique se todos os dados estão lá!

---

## 🔧 Solução de Problemas

### Erro 500 - Internal Server Error

1. Vá em **"Web"** → **"Log files"**
2. Clique em **"Error log"**
3. Veja o erro e me envie para eu te ajudar

### Banco de dados não encontrado

```bash
# No console Bash
cd ~/sistema-estoque/estoque_web
ls -la instance/
# Deve mostrar estoque.db
```

### Dependências faltando

```bash
cd ~/sistema-estoque/estoque_web
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔄 Atualizar o Sistema

Quando você fizer alterações no código:

```bash
# No console Bash
cd ~/sistema-estoque/estoque_web
git pull origin main

# Recarregar o web app
# Vá em Web → Reload
```

---

## 📊 Limitações do Plano Free

- ✅ 500MB de espaço em disco
- ✅ 100 segundos de CPU por dia
- ✅ 1 web app
- ✅ Sem hibernação
- ⚠️ Após 3 meses de inatividade, a conta é suspensa

---

## 💰 Upgrade (Opcional)

Se precisar de mais recursos:
- **Hacker Plan**: $5/mês
  - 1GB de espaço
  - Mais CPU
  - Suporte a domínio customizado

---

## 📞 Precisa de Ajuda?

- Documentação: https://help.pythonanywhere.com
- Fórum: https://www.pythonanywhere.com/forums/
- Me chame se tiver dúvidas!

---

**Boa sorte com o deploy! 🚀**

# 🚀 Guia de Deploy no Render

## Pré-requisitos
- Conta no [Render](https://render.com)
- Repositório Git (GitHub, GitLab ou Bitbucket)
- Código do projeto commitado

## 📋 Checklist Antes do Deploy

### 1. Verificar Arquivos Necessários
- ✅ `requirements.txt` - Dependências Python
- ✅ `render.yaml` - Configuração do Render
- ✅ `.env.example` - Exemplo de variáveis de ambiente
- ✅ `init_db.py` - Script de inicialização do banco
- ✅ `app.py` - Aplicação Flask

### 2. Verificar Configurações no app.py
O arquivo `app.py` já está configurado para:
- Usar PostgreSQL em produção (via DATABASE_URL)
- Usar SQLite em desenvolvimento local
- Carregar SECRET_KEY de variável de ambiente
- Configurar sessões seguras

## 🔧 Passo a Passo do Deploy

### Opção 1: Deploy via Dashboard do Render

1. **Criar Conta no Render**
   - Acesse https://render.com
   - Faça login com GitHub/GitLab

2. **Criar PostgreSQL Database**
   - No dashboard, clique em "New +"
   - Selecione "PostgreSQL"
   - Configure:
     - Name: `estoque-db`
     - Database: `estoque`
     - User: `estoque_user`
     - Region: `Oregon (US West)`
     - Plan: `Free`
   - Clique em "Create Database"
   - **IMPORTANTE**: Copie a "Internal Database URL" (será usada depois)

3. **Criar Web Service**
   - No dashboard, clique em "New +"
   - Selecione "Web Service"
   - Conecte seu repositório Git
   - Configure:
     - Name: `sistema-estoque`
     - Region: `Oregon (US West)`
     - Branch: `main`
     - Root Directory: `estoque_web`
     - Runtime: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
     - Plan: `Free`

4. **Configurar Variáveis de Ambiente**
   - Na página do Web Service, vá em "Environment"
   - Adicione as seguintes variáveis:
     ```
     SECRET_KEY = [Clique em "Generate" para criar uma chave aleatória]
     DATABASE_URL = [Cole a Internal Database URL do PostgreSQL]
     FLASK_ENV = production
     SESSION_COOKIE_SECURE = True
     PYTHON_VERSION = 3.11.0
     ```

5. **Deploy Automático**
   - O Render iniciará o deploy automaticamente
   - Aguarde a conclusão (pode levar 5-10 minutos)

6. **Inicializar o Banco de Dados**
   - Após o deploy, acesse o Shell do Web Service
   - Execute: `python init_db.py`
   - Isso criará as tabelas e dados iniciais

### Opção 2: Deploy via render.yaml (Infraestrutura como Código)

1. **Preparar o Repositório**
   - Certifique-se de que o arquivo `render.yaml` está na raiz do projeto
   - Commit e push para o repositório

2. **Criar Blueprint no Render**
   - No dashboard do Render, clique em "New +"
   - Selecione "Blueprint"
   - Conecte seu repositório
   - O Render detectará automaticamente o `render.yaml`
   - Clique em "Apply"

3. **Configurar SECRET_KEY**
   - Após a criação, vá no Web Service
   - Em "Environment", o SECRET_KEY será gerado automaticamente
   - Verifique se DATABASE_URL está conectado ao banco

4. **Inicializar o Banco**
   - Acesse o Shell do Web Service
   - Execute: `python init_db.py`

## 🔍 Verificações Pós-Deploy

1. **Testar a Aplicação**
   - Acesse a URL fornecida pelo Render (ex: `https://sistema-estoque.onrender.com`)
   - Faça login com usuário padrão: `admin` / `admin123`

2. **Verificar Logs**
   - No dashboard do Render, acesse "Logs"
   - Verifique se não há erros

3. **Testar Funcionalidades**
   - Login/Logout
   - Cadastro de produtos
   - Movimentações
   - Relatórios
   - Rankings

## ⚙️ Configurações Importantes

### Banco de Dados
- O PostgreSQL Free do Render tem limite de 1GB
- Backups automáticos não estão incluídos no plano Free
- Recomenda-se fazer backups manuais periodicamente

### Uploads de Arquivos
- Arquivos (imagens, logos) são armazenados no sistema de arquivos
- **IMPORTANTE**: No plano Free do Render, o sistema de arquivos é efêmero
- Arquivos podem ser perdidos após redeploy
- Para produção, considere usar:
  - AWS S3
  - Cloudinary
  - Outro serviço de armazenamento externo

### Sessões
- Sessões são armazenadas no servidor
- No plano Free, podem ser perdidas após inatividade

## 🔒 Segurança

1. **Alterar Senha Padrão**
   - Após o primeiro login, altere a senha do usuário admin

2. **SECRET_KEY**
   - Nunca commite a SECRET_KEY no repositório
   - Use sempre variáveis de ambiente

3. **HTTPS**
   - O Render fornece HTTPS automaticamente
   - Certifique-se de que SESSION_COOKIE_SECURE=True

## 🐛 Troubleshooting

### Erro: "Application failed to start"
- Verifique os logs no dashboard
- Confirme que todas as dependências estão no requirements.txt
- Verifique se o comando de start está correto

### Erro: "Database connection failed"
- Verifique se DATABASE_URL está configurada corretamente
- Confirme que o banco PostgreSQL está ativo
- Use a "Internal Database URL" (não a External)

### Erro: "Module not found"
- Verifique se o Root Directory está configurado como `estoque_web`
- Confirme que requirements.txt está no diretório correto

### Site muito lento
- O plano Free do Render hiberna após 15 minutos de inatividade
- O primeiro acesso após hibernação pode levar 30-60 segundos
- Considere upgrade para plano pago se necessário

## 📊 Monitoramento

- Acesse o dashboard do Render para ver:
  - Status do serviço
  - Uso de CPU e memória
  - Logs em tempo real
  - Métricas de requisições

## 🔄 Atualizações

Para atualizar o sistema:
1. Faça commit das alterações no repositório
2. Push para a branch configurada (main)
3. O Render fará deploy automático
4. Aguarde a conclusão

## 💰 Custos

### Plano Free (Atual)
- Web Service: Grátis (com limitações)
- PostgreSQL: Grátis (1GB, sem backups)
- Limitações:
  - Hiberna após 15 min de inatividade
  - 750 horas/mês de uso
  - Reinicia automaticamente

### Upgrade Recomendado
- Para uso em produção real, considere:
  - Starter Plan: $7/mês (sem hibernação)
  - PostgreSQL Starter: $7/mês (backups incluídos)

## 📞 Suporte

- Documentação oficial: https://render.com/docs
- Status do serviço: https://status.render.com
- Comunidade: https://community.render.com

---

**Última atualização**: 09/03/2026
**Versão do Sistema**: 2.0 (com Rankings de Fornecedores e Funcionários)

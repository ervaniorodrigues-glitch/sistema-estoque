# 🚀 Guia Rápido - Sistema Web de Estoque

## Primeiros Passos

### 1️⃣ Instalação Rápida
```bash
# Entrar na pasta
cd estoque_web

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Inicializar banco de dados
python init_db.py

# Executar sistema
python app.py
```

### 2️⃣ Acessar o Sistema
- URL: http://localhost:5000
- Usuário: `admin`
- Senha: `admin123`

## 📋 Funcionalidades Disponíveis

### Dashboard
- Visualize estatísticas em tempo real
- Total de produtos, funcionários, fornecedores e clientes
- Acesso rápido aos módulos

### Cadastro de Produtos
**Localização:** Menu lateral > Produtos

**Funcionalidades:**
- ➕ Adicionar novo produto
- ✏️ Editar produto existente
- 🗑️ Excluir produto
- 🔍 Buscar por código ou descrição
- 📊 Filtrar por status (Ativo/Inativo/Todos)

**Campos:**
- Código (gerado automaticamente)
- Descrição *
- Unidade (UN, KG, LT, etc)
- Marca
- Categoria
- Preço de Compra
- Preço de Venda
- Estoque Mínimo/Máximo/Atual
- Fornecedor
- Status (Ativo/Inativo)

### Cadastro de Funcionários
**Localização:** Menu lateral > Funcionários

**Funcionalidades:**
- ➕ Adicionar novo funcionário
- ✏️ Editar dados
- 🗑️ Excluir funcionário
- 🔍 Buscar por nome ou cargo
- 📊 Filtrar por status

**Campos:**
- Nome Completo *
- CPF
- Cargo *
- Data de Admissão
- Salário
- Telefone
- Email
- Endereço completo
- Status (Ativo/Inativo)

### Cadastro de Fornecedores
**Localização:** Menu lateral > Fornecedores

**Funcionalidades:**
- ➕ Adicionar novo fornecedor
- ✏️ Editar dados
- 🗑️ Excluir fornecedor
- 🔍 Buscar por nome ou CNPJ
- 📊 Filtrar por status

**Campos:**
- Nome *
- CNPJ
- Telefone
- Email
- Contato (pessoa responsável)
- Endereço completo
- Status (Ativo/Inativo)

### Cadastro de Clientes
**Localização:** Menu lateral > Clientes

**Funcionalidades:**
- ➕ Adicionar novo cliente
- ✏️ Editar dados
- 🗑️ Excluir cliente
- 🔍 Buscar por nome ou CPF/CNPJ
- 📊 Filtrar por status

**Campos:**
- Nome Completo *
- CPF/CNPJ
- Telefone
- Email
- Endereço completo
- Status (Ativo/Inativo)

## 💡 Dicas de Uso

### Busca Rápida
- Digite qualquer parte do nome, código ou documento
- A busca é instantânea (não precisa apertar Enter)
- Funciona em todos os cadastros

### Filtros de Status
- **Ativos**: Mostra apenas registros ativos
- **Inativos**: Mostra apenas registros inativos
- **Todos**: Mostra todos os registros

### Edição Rápida
1. Clique no botão ✏️ (Editar) na linha desejada
2. O modal abrirá com os dados preenchidos
3. Altere o que precisar
4. Clique em "Salvar"

### Exclusão
1. Clique no botão 🗑️ (Excluir)
2. Confirme a exclusão
3. O registro será removido permanentemente

## ⚠️ Observações Importantes

### Campos Obrigatórios
- Produtos: Código e Descrição
- Funcionários: Nome e Cargo
- Fornecedores: Nome
- Clientes: Nome

### Status Ativo/Inativo
- Registros inativos não aparecem por padrão
- Use o filtro "Inativos" ou "Todos" para visualizá-los
- Inativar é melhor que excluir (mantém histórico)

### Banco de Dados
- PostgreSQL deve estar rodando
- Credenciais configuradas em `app.py`
- Backup recomendado antes de grandes alterações

## 🔧 Configurações

### Alterar Porta do Servidor
Edite `app.py` na última linha:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Altere 5000 para outra porta
```

### Alterar Credenciais do Banco
Edite `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@localhost:5432/estoque_db'
```

## 🆘 Problemas Comuns

### Erro ao conectar no banco
- Verifique se o PostgreSQL está rodando
- Confirme usuário e senha em `app.py`
- Certifique-se que o banco `estoque_db` existe

### Página não carrega
- Verifique se o servidor Flask está rodando
- Confirme a porta (padrão: 5000)
- Limpe o cache do navegador

### Erro ao salvar
- Verifique campos obrigatórios
- Confira formato de datas e números
- Veja o console do Flask para detalhes

## 📞 Suporte
Para dúvidas ou problemas, consulte:
- README.md - Documentação completa
- INSTALACAO.md - Guia de instalação detalhado
- CHANGELOG.md - Histórico de alterações

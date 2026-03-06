# Sistema de Controle de Estoque - Versão Web

## 🚀 Tecnologias
- **Backend**: Flask (Python)
- **Banco de Dados**: PostgreSQL
- **Frontend**: Bootstrap 5 + JavaScript + Font Awesome
- **ORM**: SQLAlchemy

## 📦 Instalação

### 1. Instalar PostgreSQL
- Baixe e instale o PostgreSQL
- Crie um banco de dados chamado `estoque_db`

### 2. Configurar ambiente Python
```bash
cd estoque_web
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar banco de dados
Edite a linha no `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://seu_usuario:sua_senha@localhost:5432/estoque_db'
```

### 4. Inicializar banco de dados
```bash
python init_db.py
```

### 5. Executar aplicação
```bash
python app.py
```

Acesse: http://localhost:5000

**Login padrão:**
- Usuário: `admin`
- Senha: `admin123`

## ✅ Funcionalidades Implementadas

### Cadastros Completos
- ✅ **Produtos** - CRUD completo com busca e filtros
- ✅ **Funcionários** - Cadastro com cargo, salário, CPF
- ✅ **Fornecedores** - Cadastro com CNPJ, contato
- ✅ **Clientes** - Cadastro com CPF/CNPJ

### Sistema
- ✅ Dashboard com estatísticas em tempo real
- ✅ Sistema de login e sessão
- ✅ API REST completa
- ✅ Interface responsiva Bootstrap 5
- ✅ Filtros por status (Ativo/Inativo)
- ✅ Busca em tempo real
- ✅ Modals para edição

## 📋 Próximas Funcionalidades

### A implementar:
- [ ] Upload de fotos de produtos
- [ ] Movimentações de estoque (Entrada/Saída)
- [ ] Empréstimos de produtos
- [ ] Relatórios (Excel/PDF)
- [ ] Gráficos no dashboard
- [ ] Sistema de permissões por usuário
- [ ] Histórico de alterações
- [ ] Backup automático

## 🎨 Interface
- Design moderno com Bootstrap 5
- Sidebar com navegação intuitiva
- Cards informativos no dashboard
- Tabelas responsivas com ações
- Modals para formulários

## 📁 Estrutura do Projeto
```
estoque_web/
├── app.py              # Backend Flask
├── init_db.py          # Inicialização do banco
├── requirements.txt    # Dependências
├── templates/
│   ├── base.html       # Template base
│   ├── index.html      # Dashboard
│   ├── login.html      # Login
│   ├── produtos.html   # Cadastro de produtos
│   ├── funcionarios.html
│   ├── fornecedores.html
│   └── clientes.html
└── static/
    └── uploads/        # Fotos de produtos
```

# 🚀 Guia de Instalação - Sistema Web

## 1️⃣ Instalar PostgreSQL

1. Baixe o PostgreSQL: https://www.postgresql.org/download/
2. Instale com as configurações padrão
3. Anote a senha do usuário `postgres`

## 2️⃣ Criar Banco de Dados

Abra o pgAdmin ou terminal e execute:
```sql
CREATE DATABASE estoque_db;
```

## 3️⃣ Configurar Ambiente Python

```bash
cd estoque_web
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 4️⃣ Configurar Conexão

Edite o arquivo `app.py` na linha 18:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:SUA_SENHA@localhost:5432/estoque_db'
```

## 5️⃣ Inicializar Banco de Dados

```bash
python init_db.py
```

## 6️⃣ Executar Sistema

```bash
python app.py
```

Acesse: **http://localhost:5000**

**Login padrão:**
- Usuário: `admin`
- Senha: `admin123`

## ✅ Pronto!

O sistema está rodando! Comece cadastrando produtos.

## 📋 Funcionalidades Implementadas

- ✅ Login/Logout
- ✅ Dashboard
- ✅ Cadastro de Produtos (CRUD completo)
- ✅ Busca em tempo real
- ✅ Filtro por status (Ativo/Inativo)
- ✅ Interface responsiva
- ✅ Design moderno

## 🔜 Próximas Implementações

- Funcionários
- Fornecedores
- Clientes
- Cadastros Diversos
- Movimentações
- Empréstimos
- Relatórios

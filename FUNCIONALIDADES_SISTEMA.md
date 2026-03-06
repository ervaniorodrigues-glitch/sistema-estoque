# Funcionalidades da Página Sistema

## ✅ Implementado e Funcionando

### 🛡️ Backup e Proteção

1. **Backup Manual** ✅
   - Cria backup manual do banco de dados
   - Salva em `Backup/ManualBackup/`
   - Nome do arquivo: `estoque_web_manual_YYYYMMDD_HHMMSS.db`

2. **Listar Backups** ✅
   - Lista todos os backups disponíveis
   - Mostra nome, data e tamanho de cada backup

3. **Status do Sistema** ✅
   - Total de produtos cadastrados
   - Total de funcionários
   - Total de fornecedores
   - Total de clientes
   - Empréstimos ativos
   - Total de movimentações
   - Tamanho do banco de dados

4. **Validar Banco** ✅
   - Verifica produtos com estoque negativo
   - Verifica empréstimos com produtos inexistentes
   - Verifica movimentações com produtos inexistentes
   - Retorna lista de problemas encontrados

### 🧹 Limpeza de Dados

1. **Zerar Tudo** ✅
   - Apaga TODOS os dados do sistema
   - Mantém apenas usuários e configurações
   - Requer dupla confirmação

2. **Zerar Estoque** ✅
   - Zera apenas o estoque_atual de todos os produtos
   - Mantém os produtos cadastrados

3. **Limpar Movimentações** ✅
   - Apaga todas as movimentações de entrada/saída

4. **Limpar Cadastros** ✅
   - Zerar Produtos
   - Zerar Funcionários
   - Zerar Fornecedores
   - Zerar Clientes

5. **Limpar Empréstimos** ✅
   - Zerar Lançamentos de Empréstimo
   - Zerar Histórico de Empréstimo

### 🔧 Configurações

1. **Restaurar Backup** 🚧
   - Em desenvolvimento

2. **Configurações de Relatórios** 🚧
   - Em desenvolvimento

3. **Cadastro de Usuários** 🚧
   - Em desenvolvimento

4. **Autorização de Senhas** 🚧
   - Em desenvolvimento

5. **Limpar Histórico** 🚧
   - Em desenvolvimento

## 📋 APIs Disponíveis

### Backup
- `POST /api/backup/manual` - Criar backup manual
- `GET /api/backup/listar` - Listar backups disponíveis

### Sistema
- `GET /api/sistema/status` - Obter status do sistema
- `GET /api/sistema/validar-banco` - Validar integridade do banco

### Limpeza
- `POST /api/limpeza/tudo` - Zerar todos os dados
- `POST /api/limpeza/estoque` - Zerar estoque
- `POST /api/limpeza/movimentacoes` - Limpar movimentações
- `POST /api/limpeza/emprestimos` - Limpar empréstimos
- `POST /api/limpeza/produtos` - Limpar produtos
- `POST /api/limpeza/funcionarios` - Limpar funcionários
- `POST /api/limpeza/fornecedores` - Limpar fornecedores
- `POST /api/limpeza/clientes` - Limpar clientes

### Configurações
- `GET /api/configuracoes` - Obter configurações
- `POST /api/configuracoes` - Salvar configurações

## 🔒 Segurança

Todas as operações de limpeza requerem:
- Confirmação do usuário
- Operações críticas (Zerar Tudo) requerem dupla confirmação
- Mensagens claras sobre a irreversibilidade das ações

## 📝 Notas

- Todas as operações de limpeza são irreversíveis
- Recomenda-se fazer backup antes de qualquer operação de limpeza
- O sistema mantém usuários e configurações mesmo após "Zerar Tudo"

# Guia Rápido - Sistema Web de Estoque

## 🚀 Como Iniciar o Sistema

### Opção 1: Iniciar Manualmente
```bash
cd estoque_web
python app.py
```

### Opção 2: Usar o Script de Inicialização
```bash
python estoque_web/app.py
```

O sistema estará disponível em:
- **Local:** http://127.0.0.1:5000
- **Rede:** http://192.168.15.16:5000

## 🔐 Login

Use as credenciais configuradas no sistema desktop ou crie um novo usuário no banco de dados.

## 📦 Fluxo de Trabalho Básico

### 1. Cadastrar Produtos
1. Acesse **Produtos**
2. Clique em **Novo**
3. Preencha os dados (descrição, unidade, marca, categoria, preços, estoque)
4. Clique em **Salvar**

### 2. Cadastrar Fornecedores
1. Acesse **Fornecedores**
2. Clique em **Novo**
3. Preencha os dados (nome, telefone, email, CNPJ, etc.)
4. Clique em **Salvar**

### 3. Cadastrar Funcionários
1. Acesse **Funcionários**
2. Clique em **Novo**
3. Preencha os dados (nome, cargo, CPF, etc.)
4. Clique em **Salvar**

### 4. Entrada de Produtos (Individual)
1. Acesse **Estoque**
2. Selecione um produto na lista
3. Clique em **Entrada**
4. Preencha quantidade, fornecedor, nota fiscal
5. Clique em **Confirmar**

### 5. Entrada Múltipla de Produtos
1. Acesse **Estoque**
2. Clique em **Entrada Múltipla** (botão no topo)
3. Selecione o fornecedor
4. Adicione produtos com suas quantidades
5. Clique em **Confirmar Entrada**

### 6. Saída de Produtos
1. Acesse **Estoque**
2. Selecione um produto na lista
3. Clique em **Saída**
4. Preencha quantidade, solicitante, operação
5. Clique em **Confirmar**

### 7. Empréstimos
1. Acesse **Empréstimos**
2. Clique em **Novo Empréstimo**
3. Selecione funcionário e produto
4. Preencha observações
5. Clique em **Salvar**

### 8. Devolução de Empréstimos
1. Acesse **Empréstimos**
2. Localize o empréstimo na lista
3. Clique em **Devolver**
4. Confirme a devolução

## 📊 Relatórios e Consultas

### Movimentações
- Acesse **Movimentações**
- Use os filtros: data, tipo, mês, nota fiscal
- Exporte para Excel ou PDF

### Status do Sistema
- Acesse **Sistema**
- Clique em **Status do Sistema**
- Veja estatísticas completas

### Validar Banco
- Acesse **Sistema**
- Clique em **Validar Banco**
- Veja se há problemas de integridade

## 💾 Backup e Segurança

### Criar Backup Manual
1. Acesse **Sistema**
2. Clique em **Backup Manual**
3. Confirme a operação
4. Backup salvo em `Backup/ManualBackup/`

### Listar Backups
1. Acesse **Sistema**
2. Clique em **Listar Backups**
3. Veja todos os backups disponíveis

## 🧹 Limpeza de Dados

⚠️ **ATENÇÃO:** Todas as operações de limpeza são irreversíveis!

### Zerar Estoque
- Remove apenas o estoque_atual dos produtos
- Mantém os produtos cadastrados

### Limpar Movimentações
- Remove todas as movimentações de entrada/saída
- Não afeta o estoque atual

### Limpar Empréstimos
- Remove todos os empréstimos
- Não afeta o estoque

### Zerar Produtos/Funcionários/Fornecedores/Clientes
- Remove completamente os cadastros
- Não pode ser desfeito

### Zerar Tudo
- Remove TODOS os dados do sistema
- Mantém apenas usuários e configurações
- Requer dupla confirmação

## 🔍 Dicas e Truques

### Busca Rápida
- Use a barra de busca no topo de cada página
- Busca por código, descrição, nome, etc.

### Filtros
- Use os filtros de ativo/inativo para organizar
- Combine busca + filtros para resultados precisos

### Atalhos
- **Enter** no campo de busca = buscar
- **ESC** em modais = fechar
- Clique duplo em item da lista = editar

### Estoque Disponível
- Na página Estoque, veja "Disponível" vs "Emprestado"
- Disponível = Estoque Total - Emprestados

### Validação Automática
- Sistema valida estoque antes de empréstimos
- Impede saídas maiores que o estoque
- Valida CPF/CNPJ duplicados

## ⚠️ Avisos Importantes

1. **Backup Regular:** Faça backups frequentes!
2. **Validação:** Use "Validar Banco" periodicamente
3. **Limpeza:** Cuidado com operações de limpeza
4. **Estoque:** Sempre verifique estoque disponível antes de empréstimos
5. **Movimentações:** Registre sempre fornecedor/cliente nas movimentações

## 🆘 Solução de Problemas

### Servidor não inicia
```bash
# Verificar se a porta 5000 está em uso
netstat -ano | findstr :5000

# Matar processo se necessário
taskkill /PID <numero_do_pid> /F
```

### Erro no banco de dados
1. Acesse **Sistema** > **Validar Banco**
2. Veja os problemas encontrados
3. Corrija manualmente ou restaure backup

### Estoque negativo
1. Acesse **Sistema** > **Validar Banco**
2. Identifique produtos com estoque negativo
3. Corrija manualmente na página Produtos

### Empréstimo não permite devolução
1. Verifique se o produto ainda existe
2. Verifique se o empréstimo está com status "EMPRESTADO"
3. Use **Sistema** > **Validar Banco** para verificar

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte este guia
2. Verifique o arquivo STATUS_IMPLEMENTACAO.md
3. Use **Sistema** > **Status do Sistema** para diagnóstico
4. Use **Sistema** > **Validar Banco** para verificar integridade

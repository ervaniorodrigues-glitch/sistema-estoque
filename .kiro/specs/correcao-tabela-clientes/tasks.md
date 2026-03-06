# Implementation Plan

- [x] 1. Atualizar estrutura da tabela clientes no main.py


  - Adicionar campos celular, fax e anotacoes na definição CREATE TABLE
  - Adicionar função de migração para bancos existentes
  - A função deve verificar se cada campo existe antes de tentar adicionar
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 3.1, 3.4_



- [ ] 2. Atualizar estrutura da tabela clientes no setup_completo.py
  - Adicionar campos celular, fax e anotacoes na definição CREATE TABLE



  - Garantir que a estrutura seja idêntica à do main.py
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1_

- [ ] 3. Atualizar database_validator.py
  - Adicionar campos celular, fax e anotacoes na estrutura de validação da tabela clientes
  - Atualizar a lista de colunas essenciais para incluir os novos campos
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.2_

- [ ] 4. Implementar função de migração automática
  - Criar função migrate_clientes_table() que verifica e adiciona campos faltantes
  - Usar PRAGMA table_info para verificar campos existentes
  - Usar ALTER TABLE ADD COLUMN para adicionar campos faltantes
  - Implementar tratamento de erros para colunas já existentes
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 5. Integrar migração na inicialização do sistema
  - Chamar migrate_clientes_table() após criar/verificar tabelas no main.py
  - Garantir que a migração seja executada antes de qualquer operação com clientes
  - Adicionar logging para rastrear migrações executadas
  - _Requirements: 3.1, 3.2_

- [ ] 6. Criar testes de validação
  - [ ] 6.1 Testar criação de tabela nova com todos os campos
    - Criar banco de dados vazio
    - Executar inicialização
    - Verificar que todos os campos existem
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ] 6.2 Testar migração de banco existente
    - Criar banco com estrutura antiga (sem celular, fax, anotacoes)
    - Adicionar dados de teste
    - Executar migração
    - Verificar que campos foram adicionados e dados preservados
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ] 6.3 Testar idempotência da migração
    - Executar migração duas vezes no mesmo banco
    - Verificar que não há erros
    - Verificar que estrutura está correta
    - _Requirements: 3.4_

- [ ] 7. Checkpoint - Verificar funcionamento completo
  - Testar cadastro de novo cliente com todos os campos
  - Testar edição de cliente existente
  - Verificar que não há erros de campo inexistente
  - Ensure all tests pass, ask the user if questions arise.

# Documento de Design

## Visão Geral

O sistema será estendido para incluir botões de "Limpeza Geral" em cada um dos três grupos principais da interface (Cadastros, Movimentações, Relatórios). Cada botão abrirá uma janela específica com opções de limpeza e manutenção adequadas para sua área, mantendo o layout visual consistente com o sistema existente.

## Arquitetura

### Estrutura de Classes

```
SistemaEstoque (main.py)
├── LimpezaCadastros (novo módulo)
├── LimpezaMovimentacoes (novo módulo)
├── LimpezaRelatorios (novo módulo)
└── BackupManager (utilitário para backups automáticos)
```

### Fluxo de Dados

1. **Interface Principal**: Botões adicionados aos grupos existentes
2. **Módulos de Limpeza**: Classes específicas para cada tipo de limpeza
3. **Backup Automático**: Sistema de backup antes de operações críticas
4. **Relatórios de Limpeza**: Feedback detalhado das operações realizadas

## Componentes e Interfaces

### 1. Interface Principal (main.py)

**Modificações necessárias:**
- Adicionar botão "Limpeza Geral" em cada grupo
- Manter layout visual consistente com botões existentes
- Conectar botões aos respectivos módulos de limpeza

**Layout dos botões:**
```
Grupo Cadastros:          Grupo Movimentações:      Grupo Relatórios:
- Produtos               - Lançamentos             - Posição Estoque
- Fornecedores          - Empréstimos             - Movimentações  
- Clientes              - Retiradas               - Busca
- Limpeza Geral         - Limpeza Geral           - Limpeza Geral
```

### 2. Módulo LimpezaCadastros

**Funcionalidades:**
- Remoção de produtos duplicados
- Remoção de fornecedores duplicados  
- Remoção de clientes duplicados
- Correção de dados inconsistentes
- Relatório de limpeza

**Interface:**
- Janela modal com checkboxes para cada opção
- Botões: Executar, Relatório, Fechar
- Barra de progresso para operações longas

### 3. Módulo LimpezaMovimentacoes

**Funcionalidades:**
- Arquivamento de movimentações antigas
- Remoção de lançamentos duplicados
- Correção de saldos de estoque
- Limpeza de empréstimos finalizados
- Backup automático antes das operações

**Interface:**
- Janela modal com opções de data para arquivamento
- Checkboxes para tipos de limpeza
- Confirmação obrigatória para operações críticas

### 4. Módulo LimpezaRelatorios

**Funcionalidades:**
- Limpeza de arquivos temporários
- Otimização de índices do banco
- Limpeza de cache de consultas
- Estatísticas de uso do sistema
- Relatório de otimização

**Interface:**
- Janela modal com opções de otimização
- Exibição de estatísticas do sistema
- Botões para diferentes tipos de otimização

## Modelos de Dados

### Tabela de Logs de Limpeza
```sql
CREATE TABLE logs_limpeza (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_limpeza TEXT NOT NULL,
    operacao TEXT NOT NULL,
    registros_afetados INTEGER,
    detalhes TEXT,
    usuario TEXT DEFAULT 'Administrador'
)
```

### Estrutura de Backup
- Backup automático antes de operações críticas
- Nomenclatura: `backup_limpeza_YYYYMMDD_HHMMSS.db`
- Armazenamento em pasta `backups/`

## Tratamento de Erros

### Estratégias de Erro

1. **Backup Automático**: Antes de qualquer operação crítica
2. **Rollback**: Restauração automática em caso de erro
3. **Validação**: Verificação de integridade antes e depois
4. **Logs Detalhados**: Registro de todas as operações

### Cenários de Erro

- **Falha na operação**: Restaurar backup automaticamente
- **Dados corrompidos**: Validar integridade e alertar usuário
- **Falta de espaço**: Verificar espaço disponível antes da operação
- **Banco bloqueado**: Aguardar liberação ou alertar usuário

## Estratégia de Testes

### Testes Unitários
- Validação de cada função de limpeza
- Testes de backup e restauração
- Verificação de integridade dos dados

### Testes de Integração
- Fluxo completo de limpeza
- Interação entre módulos
- Validação de interface

### Testes de Segurança
- Proteção contra perda de dados
- Validação de backups
- Recuperação de falhas

## Considerações de Performance

### Otimizações
- Operações em lote para grandes volumes
- Índices otimizados para consultas de limpeza
- Processamento assíncrono para operações longas

### Monitoramento
- Barra de progresso para operações longas
- Estimativa de tempo restante
- Cancelamento de operações em andamento

## Padrões de Interface

### Consistência Visual
- Mesmo estilo de botões do sistema existente
- Cores e fontes padronizadas (#f0f0f0, Arial)
- Layout similar às janelas existentes

### Usabilidade
- Confirmações claras para operações críticas
- Feedback visual durante processamento
- Relatórios detalhados pós-operação

### Acessibilidade
- Atalhos de teclado
- Mensagens claras e informativas
- Operações reversíveis quando possível
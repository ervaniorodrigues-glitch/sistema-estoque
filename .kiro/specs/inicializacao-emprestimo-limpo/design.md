# Design Document

## Overview

O sistema de inicialização limpa de empréstimos é projetado para garantir que o módulo de empréstimos seja iniciado com uma tabela completamente vazia, mantendo a integridade estrutural e funcional do sistema. A solução modifica o comportamento de inicialização existente para incluir uma limpeza automática dos dados de empréstimos.

## Architecture

### Componente Principal
- **EmprestimosInitializer**: Classe responsável pela inicialização limpa do sistema
- **DatabaseManager**: Gerenciador de operações de banco de dados
- **InterfaceController**: Controlador da interface gráfica

### Fluxo de Inicialização
```
Início → Verificar Estrutura DB → Limpar Dados → Carregar Interface → Pronto
```

## Components and Interfaces

### 1. EmprestimosInitializer

**Responsabilidades:**
- Verificar existência da estrutura do banco
- Executar limpeza completa da tabela de empréstimos
- Validar integridade após limpeza
- Registrar operações no log

**Métodos principais:**
```python
class EmprestimosInitializer:
    def __init__(self, db_path: str)
    def verificar_estrutura_banco(self) -> bool
    def limpar_tabela_emprestimos(self) -> bool
    def validar_integridade_pos_limpeza(self) -> bool
    def executar_inicializacao_limpa(self) -> bool
```

### 2. DatabaseManager

**Responsabilidades:**
- Executar comandos SQL de limpeza
- Verificar estrutura das tabelas
- Manter integridade referencial

**Métodos principais:**
```python
class DatabaseManager:
    def criar_estrutura_emprestimos(self) -> bool
    def limpar_dados_emprestimos(self) -> bool
    def verificar_tabelas_relacionadas(self) -> bool
    def obter_proximo_codigo(self) -> int
```

### 3. InterfaceController

**Responsabilidades:**
- Inicializar interface com dados limpos
- Configurar campos padrão
- Carregar dados de referência (funcionários, produtos)

**Métodos principais:**
```python
class InterfaceController:
    def inicializar_campos_limpos(self) -> None
    def carregar_dados_referencia(self) -> None
    def configurar_grid_vazio(self) -> None
    def definir_valores_padrao(self) -> None
```

## Data Models

### Estrutura da Tabela Empréstimos (Mantida)
```sql
CREATE TABLE emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    funcionario TEXT NOT NULL,
    cargo TEXT,
    cod_produto TEXT NOT NULL,
    descricao_item TEXT NOT NULL,
    observacoes TEXT,
    status TEXT DEFAULT 'EMPRESTADO',
    data_cadastro TEXT NOT NULL
);
```

### Tabelas Relacionadas (Preservadas)
- **funcionarios**: Mantida intacta
- **produtos**: Mantida intacta
- **movimentacoes**: Mantida intacta (apenas empréstimos são limpos)

## Error Handling

### Estratégias de Tratamento de Erros

1. **Erro de Conexão com Banco**
   - Tentar reconectar até 3 vezes
   - Exibir mensagem de erro específica
   - Permitir retry manual

2. **Erro na Limpeza de Dados**
   - Fazer rollback da transação
   - Registrar erro no log
   - Manter dados existentes se limpeza falhar

3. **Erro de Integridade**
   - Validar estrutura antes de prosseguir
   - Recriar tabela se necessário
   - Notificar sobre problemas estruturais

4. **Erro na Interface**
   - Carregar interface com valores padrão
   - Desabilitar funcionalidades problemáticas
   - Permitir operação manual

### Logging e Monitoramento
```python
# Níveis de log implementados
INFO: "Inicialização limpa executada com sucesso"
WARNING: "Tabela já estava vazia"
ERROR: "Falha na limpeza: [detalhes]"
DEBUG: "Estrutura verificada: [status]"
```

## Testing Strategy

### Testes Unitários
1. **Teste de Limpeza de Dados**
   - Verificar remoção completa de registros
   - Validar preservação da estrutura
   - Confirmar integridade após limpeza

2. **Teste de Inicialização**
   - Verificar criação de estrutura quando não existe
   - Validar comportamento com banco vazio
   - Testar recuperação de erros

3. **Teste de Interface**
   - Verificar carregamento com dados limpos
   - Validar valores padrão dos campos
   - Confirmar funcionalidade do grid vazio

### Testes de Integração
1. **Teste de Fluxo Completo**
   - Executar inicialização limpa
   - Criar novo empréstimo
   - Verificar funcionamento normal

2. **Teste de Preservação de Dados**
   - Confirmar que funcionários são mantidos
   - Verificar que produtos são preservados
   - Validar outras tabelas intactas

### Cenários de Teste
1. **Banco Novo (Primeira Execução)**
   - Sistema cria estrutura completa
   - Interface carrega corretamente
   - Primeiro empréstimo funciona

2. **Banco Existente com Dados**
   - Dados de empréstimos são removidos
   - Outras tabelas são preservadas
   - Interface carrega limpa

3. **Banco Corrompido**
   - Sistema detecta problemas
   - Tenta recuperar estrutura
   - Notifica sobre problemas

## Implementation Notes

### Modificações no Código Existente

1. **emprestimos.py**
   - Adicionar chamada para inicialização limpa no método `__init__`
   - Modificar `criar_tabelas_vazias()` para usar novo sistema
   - Integrar logging de operações

2. **Novo Módulo: emprestimos_initializer.py**
   - Implementar toda lógica de inicialização limpa
   - Centralizar operações de banco relacionadas à limpeza
   - Fornecer interface clara para outros módulos

### Configurações
- **AUTO_CLEAN_ON_START**: Flag para controlar limpeza automática
- **BACKUP_BEFORE_CLEAN**: Opção de backup antes da limpeza
- **LOG_LEVEL**: Nível de detalhamento do log

### Performance Considerations
- Operação de limpeza deve ser rápida (< 1 segundo)
- Usar transações para garantir atomicidade
- Minimizar operações de I/O durante inicialização
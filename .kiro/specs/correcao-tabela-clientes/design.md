# Design Document

## Overview

Este design especifica como corrigir a estrutura da tabela `clientes` no banco de dados SQLite para que tenha a mesma estrutura completa que a tabela `funcionarios`, mas com campos apropriados para clientes. A tabela `clientes` está faltando os campos `celular`, `fax` e `anotacoes` que são utilizados pela interface de cadastro.

## Architecture

O sistema utiliza SQLite como banco de dados e possui múltiplos pontos onde a estrutura da tabela `clientes` é definida ou referenciada:

1. **main.py** - Inicialização principal do banco de dados
2. **setup_completo.py** - Script de setup inicial
3. **database_validator.py** - Validação e correção de estrutura
4. **cadastro_clientes_completo.py** - Interface de cadastro que usa os campos

A correção será implementada através de:
- Atualização das definições CREATE TABLE em todos os arquivos
- Adição de lógica de migração para bancos existentes
- Validação automática da estrutura na inicialização

## Components and Interfaces

### 1. Database Schema Update

A estrutura completa da tabela `clientes` deve seguir o mesmo padrão da tabela `funcionarios`:

**Tabela FUNCIONARIOS (referência):**
```sql
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cargo TEXT,
    telefone TEXT,
    email TEXT,
    endereco TEXT,
    cidade TEXT,
    uf TEXT,
    cep TEXT,
    cpf TEXT,
    data_admissao TEXT,
    salario REAL,
    ativo INTEGER DEFAULT 1
)
```

**Tabela CLIENTES (corrigida):**
```sql
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT,
    telefone TEXT,
    celular TEXT,
    fax TEXT,
    endereco TEXT,
    cidade TEXT,
    uf TEXT,
    cep TEXT,
    anotacoes TEXT,
    ativo INTEGER DEFAULT 1
)
```

**Campos faltantes a adicionar:**
- `celular TEXT` - Telefone celular do cliente
- `fax TEXT` - Número de fax do cliente  
- `anotacoes TEXT` - Observações sobre o cliente

### 2. Migration Logic

Para bancos de dados existentes, será necessário:

```python
def migrate_clientes_table(cursor):
    """Add missing columns to clientes table"""
    # Check and add celular
    # Check and add fax
    # Check and add anotacoes
    # Check and add cep (if missing)
```

### 3. Files to Update

- `main.py` - Atualizar CREATE TABLE e adicionar migração
- `setup_completo.py` - Atualizar CREATE TABLE
- `database_validator.py` - Atualizar estrutura de validação

## Data Models

### Cliente Model (Updated)

```python
{
    "id": int,              # Primary key, auto-increment
    "nome": str,            # Required, not null
    "email": str,           # Optional
    "telefone": str,        # Optional (telefone comercial)
    "celular": str,         # Optional (NEW - telefone celular)
    "fax": str,             # Optional (NEW - número de fax)
    "endereco": str,        # Optional
    "cidade": str,          # Optional
    "uf": str,              # Optional
    "cep": str,             # Optional
    "anotacoes": str,       # Optional (NEW - observações)
    "ativo": int            # Default 1
}
```

**Comparação com Funcionarios:**
- Funcionarios tem: cargo, cpf, data_admissao, salario
- Clientes tem: celular, fax, anotacoes
- Ambos compartilham: id, nome, telefone, email, endereco, cidade, uf, cep, ativo

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Required fields exist after initialization
*For any* database after initialization, querying the clientes table structure should return the celular, fax, and anotacoes fields.
**Validates: Requirements 1.1, 1.2, 1.3**

### Property 2: CEP field exists
*For any* database after initialization, querying the clientes table structure should return the cep field.
**Validates: Requirements 1.4**

### Property 3: Data preservation during migration
*For any* existing database with cliente records, after running the migration, all original field values should remain unchanged.
**Validates: Requirements 1.5, 3.2**

### Property 4: Interface field access succeeds
*For any* operation in cadastro_clientes_completo.py that accesses a database field, the operation should complete without database field errors.
**Validates: Requirements 2.3**

### Property 5: Migration adds missing columns
*For any* database missing the celular, fax, or anotacoes columns, after running the migration, those columns should exist in the clientes table.
**Validates: Requirements 3.1**

### Property 6: New columns have appropriate defaults
*For any* existing cliente record after migration, the newly added columns (celular, fax, anotacoes) should have NULL values.
**Validates: Requirements 3.3**

### Property 7: Migration idempotency
*For any* database, running the migration multiple times should not cause errors and should result in the same correct schema.
**Validates: Requirements 3.4**

## Error Handling

### Migration Errors
- If ALTER TABLE fails, log the error and continue with other columns
- If a column already exists, skip it silently (no error)
- If database is locked, retry up to 3 times with 1 second delay

### Validation Errors
- If table doesn't exist, create it with full schema
- If critical fields are missing (id, nome), recreate the table
- Log all schema inconsistencies for review

## Testing Strategy

### Unit Tests
- Test migration function with various database states
- Test schema validation logic
- Test error handling for locked databases

### Integration Tests  
- Test full initialization flow with new database
- Test migration flow with existing database
- Test cadastro_clientes_completo.py operations after migration

### Manual Testing
- Verify existing cliente data is preserved
- Verify new fields appear in cadastro interface
- Verify no errors when saving clientes with new fields


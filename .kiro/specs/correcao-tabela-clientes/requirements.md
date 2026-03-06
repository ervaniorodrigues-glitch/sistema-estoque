# Requirements Document

## Introduction

Este documento especifica os requisitos para corrigir a estrutura da tabela `clientes` no banco de dados SQLite, adicionando os campos faltantes que são utilizados pela interface de cadastro de clientes mas não existem na estrutura da tabela.

## Glossary

- **Sistema**: O sistema de controle de estoque
- **Tabela Clientes**: Tabela do banco de dados SQLite que armazena informações dos clientes
- **Campo**: Coluna em uma tabela de banco de dados
- **Migração**: Processo de alteração da estrutura do banco de dados

## Requirements

### Requirement 1

**User Story:** Como desenvolvedor, eu quero que a tabela `clientes` tenha todos os campos necessários, para que a interface de cadastro funcione corretamente sem erros.

#### Acceptance Criteria

1. WHEN the system initializes the database THEN the clientes table SHALL include the celular field
2. WHEN the system initializes the database THEN the clientes table SHALL include the fax field  
3. WHEN the system initializes the database THEN the clientes table SHALL include the anotacoes field
4. WHEN the system initializes the database THEN the clientes table SHALL include the cep field
5. WHEN the system initializes the database THEN all existing fields SHALL remain unchanged

### Requirement 2

**User Story:** Como desenvolvedor, eu quero que a estrutura da tabela `clientes` seja consistente em todos os arquivos do sistema, para que não haja discrepâncias entre diferentes partes do código.

#### Acceptance Criteria

1. WHEN the database structure is defined in main.py THEN it SHALL match the structure in setup_completo.py
2. WHEN the database structure is defined in database_validator.py THEN it SHALL match the structure in main.py
3. WHEN the cadastro_clientes_completo.py accesses a field THEN that field SHALL exist in the database table

### Requirement 3

**User Story:** Como desenvolvedor, eu quero que bancos de dados existentes sejam migrados automaticamente, para que usuários existentes não percam dados ao atualizar o sistema.

#### Acceptance Criteria

1. WHEN the system detects missing columns in an existing database THEN it SHALL add those columns using ALTER TABLE
2. WHEN new columns are added THEN existing data SHALL be preserved
3. WHEN new columns are added THEN they SHALL have appropriate default values
4. IF a column already exists THEN the system SHALL not attempt to add it again

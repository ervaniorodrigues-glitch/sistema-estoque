# Requirements Document

## Introduction

Este documento especifica os requisitos para corrigir o problema de rotas não registradas no sistema web de controle de estoque. Atualmente, a rota `/cadastros-diversos` e suas APIs relacionadas (unidades, marcas, categorias e operações) não estão acessíveis porque foram definidas após o bloco de inicialização do Flask, impedindo seu registro adequado.

## Glossary

- **Flask Application**: O servidor web Flask que gerencia as rotas HTTP
- **Route Registration**: O processo pelo qual o Flask registra endpoints HTTP para serem acessíveis
- **Cadastros Diversos**: Módulo que gerencia entidades auxiliares (unidades, marcas, categorias, operações)
- **API Endpoint**: Uma rota HTTP que retorna dados em formato JSON

## Requirements

### Requirement 1

**User Story:** Como desenvolvedor, eu quero que todas as rotas sejam registradas corretamente no Flask, para que os usuários possam acessar todas as funcionalidades do sistema.

#### Acceptance Criteria

1. WHEN the Flask application starts THEN the system SHALL register all route handlers before the application initialization block
2. WHEN a user accesses `/cadastros-diversos` THEN the system SHALL return the cadastros_diversos.html template
3. WHEN the application code is organized THEN the system SHALL place all route definitions before the `if __name__ == '__main__'` block
4. WHEN the server starts THEN the system SHALL make all API endpoints accessible at their defined paths

### Requirement 2

**User Story:** Como usuário do sistema, eu quero acessar a página de cadastros diversos, para que eu possa gerenciar unidades, marcas, categorias e operações.

#### Acceptance Criteria

1. WHEN a user navigates to `/cadastros-diversos` THEN the system SHALL display the cadastros diversos interface
2. WHEN the page loads THEN the system SHALL provide access to manage unidades, marcas, categorias, and operações
3. WHEN a user is not authenticated THEN the system SHALL redirect to the login page
4. WHEN the page renders THEN the system SHALL load all existing data from the database

### Requirement 3

**User Story:** Como usuário, eu quero gerenciar unidades de medida, para que eu possa categorizar produtos corretamente.

#### Acceptance Criteria

1. WHEN a user requests `/api/unidades` with GET THEN the system SHALL return all unidades ordered by name
2. WHEN a user posts to `/api/unidades` with valid data THEN the system SHALL create a new unidade
3. WHEN a user attempts to create a duplicate unidade THEN the system SHALL reject the request and return an error message
4. WHEN a user deletes an unidade via `/api/unidades/<id>` THEN the system SHALL remove it from the database

### Requirement 4

**User Story:** Como usuário, eu quero gerenciar marcas de produtos, para que eu possa organizar o catálogo por fabricante.

#### Acceptance Criteria

1. WHEN a user requests `/api/marcas` with GET THEN the system SHALL return all marcas ordered by name
2. WHEN a user posts to `/api/marcas` with valid data THEN the system SHALL create a new marca
3. WHEN a user attempts to create a duplicate marca THEN the system SHALL reject the request and return an error message
4. WHEN a user deletes a marca via `/api/marcas/<id>` THEN the system SHALL remove it from the database

### Requirement 5

**User Story:** Como usuário, eu quero gerenciar categorias de produtos, para que eu possa classificar o inventário de forma lógica.

#### Acceptance Criteria

1. WHEN a user requests `/api/categorias` with GET THEN the system SHALL return all categorias ordered by name
2. WHEN a user posts to `/api/categorias` with valid data THEN the system SHALL create a new categoria
3. WHEN a user attempts to create a duplicate categoria THEN the system SHALL reject the request and return an error message
4. WHEN a user deletes a categoria via `/api/categorias/<id>` THEN the system SHALL remove it from the database

### Requirement 6

**User Story:** Como usuário, eu quero gerenciar tipos de operações, para que eu possa registrar diferentes tipos de movimentações de estoque.

#### Acceptance Criteria

1. WHEN a user requests `/api/operacoes` with GET THEN the system SHALL return all operações ordered by name
2. WHEN a user posts to `/api/operacoes` with valid data THEN the system SHALL create a new operação
3. WHEN a user attempts to create a duplicate operação THEN the system SHALL reject the request and return an error message
4. WHEN a user deletes an operação via `/api/operacoes/<id>` THEN the system SHALL remove it from the database

# Design Document

## Overview

This design addresses the route registration issue in the Flask application where the `/cadastros-diversos` route and related API endpoints are defined after the `if __name__ == '__main__'` block, preventing them from being registered. The solution involves reorganizing the code structure to ensure all routes are defined before application initialization.

## Architecture

The Flask application follows a monolithic architecture with:
- Route handlers defined as decorated functions
- SQLAlchemy models for database entities
- Session-based authentication
- JSON API endpoints for CRUD operations

The fix requires moving route definitions to their proper location in the file structure, ensuring Flask's route registration mechanism can process them during application startup.

## Components and Interfaces

### Affected Components

1. **Flask Application (app.py)**
   - Main application file containing all routes
   - Needs reorganization to place routes before initialization block

2. **Route Handlers**
   - `/cadastros-diversos` - Main page route
   - `/api/unidades` - Unidades CRUD endpoints
   - `/api/marcas` - Marcas CRUD endpoints
   - `/api/categorias` - Categorias CRUD endpoints
   - `/api/operacoes` - Operações CRUD endpoints

### File Structure

The corrected structure should be:
```
1. Imports
2. Flask app initialization
3. Database configuration
4. Model definitions
5. ALL route handlers (including cadastros diversos)
6. if __name__ == '__main__': block
```

## Data Models

No changes to existing models are required. The following models are already defined and will continue to work:

- `Unidade` - Stores measurement units
- `Marca` - Stores product brands
- `Categoria` - Stores product categories
- `Operacao` - Stores operation types

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After analyzing all acceptance criteria, several patterns emerged that apply uniformly across all cadastros diversos entities (unidades, marcas, categorias, operações). Rather than creating separate properties for each entity type, we consolidate into generic properties that validate the CRUD operations work correctly for any entity type.

Property 1: API endpoints return ordered results
*For any* cadastros diversos entity type (unidades, marcas, categorias, operações), when requesting the list endpoint, the system should return all entities ordered alphabetically by name
**Validates: Requirements 3.1, 4.1, 5.1, 6.1**

Property 2: Create operation persists entities
*For any* cadastros diversos entity type and any valid entity data, when posting to the create endpoint, the system should persist the entity and return it in subsequent list requests
**Validates: Requirements 3.2, 4.2, 5.2, 6.2**

Property 3: Delete operation removes entities
*For any* cadastros diversos entity type and any existing entity, when deleting via the delete endpoint, the system should remove the entity and it should not appear in subsequent list requests
**Validates: Requirements 3.4, 4.4, 5.4, 6.4**

Example 1: Cadastros diversos page is accessible
When an authenticated user navigates to `/cadastros-diversos`, the system should return HTTP 200 with the cadastros_diversos.html template
**Validates: Requirements 1.2, 2.1**

Example 2: Unauthenticated access redirects to login
When a user without session credentials accesses `/cadastros-diversos`, the system should redirect to `/login`
**Validates: Requirements 2.3**

Example 3: Duplicate entities are rejected
When attempting to create a unidade with a name that already exists, the system should return an error response and not create a duplicate entry
**Validates: Requirements 3.3, 4.3, 5.3, 6.3**

## Error Handling

The application should handle the following error scenarios:

1. **Duplicate Entity Names**: When attempting to create an entity with a name that already exists, the system should:
   - Rollback the database transaction
   - Return a JSON response with `success: False`
   - Include an appropriate error message

2. **Missing Authentication**: When accessing protected routes without authentication:
   - Redirect to the login page
   - Preserve the original URL for post-login redirect (optional enhancement)

3. **Entity Not Found**: When attempting to delete a non-existent entity:
   - Return HTTP 404 via Flask's `get_or_404()` method
   - Provide clear error message

4. **Database Errors**: When database operations fail:
   - Rollback transactions to maintain data integrity
   - Return appropriate error responses
   - Log errors for debugging

## Testing Strategy

### Unit Testing

We will use pytest with Flask's test client to verify:

- Route accessibility (all endpoints return appropriate status codes)
- Authentication requirements (protected routes redirect when not authenticated)
- Specific edge cases like duplicate entity creation

### Property-Based Testing

We will use Hypothesis (Python's property-based testing library) to verify:

- CRUD operations work correctly across all entity types with randomly generated data
- List endpoints always return results in alphabetical order
- Create-then-read operations are consistent
- Delete operations properly remove entities

**Configuration**: Each property-based test will run a minimum of 100 iterations to ensure thorough coverage of the input space.

**Test Tagging**: Each property-based test will include a comment in this format:
```python
# Feature: correcao-rotas-cadastros-diversos, Property 1: API endpoints return ordered results
```

### Integration Testing

- Verify the complete flow: create entity → list entities → delete entity
- Test cross-entity interactions if applicable
- Verify database state after operations

## Implementation Notes

### Code Organization Fix

The primary fix involves moving the cadastros diversos routes from their current position (after `if __name__ == '__main__'`) to before the initialization block. The corrected structure:

```python
# ... existing routes (funcionarios, fornecedores, clientes, produtos) ...

# ==================== CADASTROS DIVERSOS ====================
@app.route('/cadastros-diversos')
def cadastros_diversos():
    # ... implementation ...

# All API routes for unidades, marcas, categorias, operações
# ... 

# ==================== APPLICATION STARTUP ====================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### No Breaking Changes

This fix is purely organizational and does not modify:
- Database models
- API contracts
- Frontend templates
- Existing functionality

### Verification

After the fix, verify:
1. Server starts without errors
2. `/cadastros-diversos` returns HTTP 200 (not 404)
3. All API endpoints respond correctly
4. Existing routes continue to work

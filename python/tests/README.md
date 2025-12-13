# Test Suite Documentation

This directory contains comprehensive tests for the User, Company, and Transaction CRUD operations.

## Test Coverage

### Test Files

1. **`test_user_crud.py`** - 30 tests covering:
   - User creation (11 tests): Basic, minimal, edge cases (negative balance, large values, special characters, etc.)
   - User reading (7 tests): Get single user, get all users, pagination, non-existent users
   - User updating (5 tests): Full update, partial update, edge cases
   - User deletion (3 tests): Delete existing, delete non-existent, delete with transactions (cascade)

2. **`test_company_crud.py`** - 23 tests covering:
   - Company creation (8 tests): Basic, minimal, edge cases (long strings, special characters, empty strings)
   - Company reading (7 tests): Get single company, get all companies, pagination
   - Company updating (5 tests): Full update, partial update, edge cases
   - Company deletion (3 tests): Delete existing, delete non-existent, delete with transactions (cascade)

3. **`test_transaction_crud.py`** - 22 tests covering:
   - Transaction creation (8 tests): Basic, with datetime, edge cases (zero/negative/large shares, multiple users/companies)
   - Transaction reading (9 tests): Get single, get all, filter by user, filter by company, filter by both
   - Transaction updating (4 tests): Full update, partial update, edge cases
   - Transaction deletion (3 tests): Delete existing, delete non-existent, delete multiple

4. **`test_crud_order.py`** - 10 tests covering:
   - Standard CRUD sequences
   - Multiple updates
   - Create-delete-create patterns
   - User-company-transaction chains
   - Cascade deletions
   - Complex workflows
   - Bulk operations
   - Foreign key integrity

## Running Tests

### Run all tests:
```bash
python -m pytest tests/ -v
```

### Run specific test file:
```bash
python -m pytest tests/test_user_crud.py -v
```

### Run specific test class:
```bash
python -m pytest tests/test_user_crud.py::TestUserCreate -v
```

### Run specific test:
```bash
python -m pytest tests/test_user_crud.py::TestUserCreate::test_create_user_basic -v
```

### Run with coverage:
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

## Test Statistics

- **Total Tests**: 85
- **All Passing**: ✅
- **Test Categories**:
  - User CRUD: 30 tests
  - Company CRUD: 23 tests
  - Transaction CRUD: 22 tests
  - CRUD Order/Workflow: 10 tests

## Edge Cases Covered

### User Edge Cases:
- Negative balances
- Very large balances
- Zero balances
- Old and future dates
- Long addresses (500+ characters)
- Special characters in names
- Empty ID lookups
- Deletion with related transactions

### Company Edge Cases:
- Long names and locations (500+ characters)
- Special characters
- Empty strings
- Numbers in names
- Deletion with related transactions

### Transaction Edge Cases:
- Zero shares
- Negative shares
- Very large share counts
- Multiple users with same company
- Same user with multiple companies
- Transactions with specific datetimes
- Filtering by non-existent users/companies

### Workflow Edge Cases:
- Multiple sequential updates
- Create-delete-create patterns
- Cascade deletions
- Complex multi-entity workflows
- Bulk operations
- Foreign key integrity maintenance

## Test Fixtures

The `conftest.py` file provides:
- `db_session`: A fresh in-memory SQLite database for each test, ensuring test isolation

## Notes

- All tests use an in-memory database, so they don't affect the production database
- Each test gets a fresh database session, ensuring no test pollution
- Tests cover both happy paths and error cases
- Foreign key relationships and cascade deletions are thoroughly tested


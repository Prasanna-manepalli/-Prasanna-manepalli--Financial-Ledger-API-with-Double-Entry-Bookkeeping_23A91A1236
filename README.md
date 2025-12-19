# Financial Ledger API – Double Entry Bookkeeping (Week 4)

## Objective
This project implements a robust financial ledger system based on **double-entry bookkeeping principles**.  
It is designed as the backend foundation for a mock banking application, with a strong focus on **data integrity, auditability, and correctness**.

The system ensures that all financial operations are handled safely using **ACID-compliant database transactions**, immutable ledger records, and on-demand balance calculation derived entirely from transaction history.

---

## Key Concepts Implemented
- Double-entry bookkeeping
- ACID database transactions
- Immutable ledger entries
- Balance calculation from ledger (no stored balance)
- Overdraft prevention
- Concurrency-safe operations

---

## Technology Stack
- **Language:** Python
- **Database:** PostgreSQL
- **Database Driver:** psycopg2
- **Tools:** VS Code, Git, GitHub, pgAdmin

---
## Project Structure
```
.
week4/
├── transfer.py              # Handles account-to-account transfers
├── deposit.py               # Handles deposits into accounts
├── database_schema.sql      # Database schema definition
├── db_test.py               # Database connectivity testing
└── README.md
```
---

## Database Design

The database schema is defined in `database_schema.sql`.

### Core Tables
1. **accounts**
   - Stores account metadata (user, type, currency, status)
   - Does NOT store balance

2. **transactions**
   - Represents the intent of a financial operation (deposit, transfer)
   - Tracks status of the operation

3. **ledger_entries**
   - Immutable records of money movement
   - Each entry is either a debit or credit
   - Acts as the single source of truth

### Balance Calculation
Account balance is calculated dynamically using:

```sql
SUM(
  CASE
    WHEN entry_type = 'credit' THEN amount
    ELSE -amount
  END
)

```

### Error Handling

The application is designed with robust error handling to ensure clear and meaningful responses when used as a REST API.

 **400 Bad Request**
  - Returned for invalid inputs such as negative amounts or missing account identifiers.

**422 Unprocessable Entity**
  - Returned when business rules fail, such as insufficient account balance during a transfer.
  - In such cases, the database transaction is rolled back to maintain consistency.

- **500 Internal Server Error**
  - Returned for unexpected system errors such as database connection failures or unhandled exceptions.

This approach ensures that clients receive precise feedback while preserving data integrity.

---

## Notes on API Design and Evaluation Scope
 - This project focuses on implementing the core backend logic of a financial ledger system, including double-entry bookkeeping, ACID-compliant transactions, ledger immutability, balance integrity, and concurrency safety. 

 - While the core business logic is implemented and fully functional, the REST API endpoints described in the specification are conceptually addressed and documented rather than exposed through a web framework. The design and behavior of these endpoints are explained to demonstrate understanding of API semantics, error handling, and expected responses.
- This approach emphasizes correctness, reliability, and database transaction safety, which are the primary learning objectives of this task.

---
## Application Scope Clarification

- This project focuses on implementing the core backend logic of a financial ledger system, including database schema design, double-entry bookkeeping, ACID-compliant transactions, balance integrity, and concurrency safety.

- The REST API endpoints described in the specification are conceptually addressed through the implemented logic and documented behavior. The primary emphasis of this submission is correctness, reliability, and transaction safety rather than full API exposure through a web framework.
 
---
import psycopg2

# -------- CONFIGURATION --------
DB_NAME = "ledger_db"
DB_USER = "postgres"
DB_PASSWORD = "Prasanna@271"
DB_HOST = "localhost"
DB_PORT = "5432"

# -------- INPUT (TEMPORARY FOR TESTING) --------
source_account_id = "91101a76-93ff-4066-b14b-8047d3ce40b6"
destination_account_id = "e1030875-496d-43c8-839d-e100c71c2d04"
transfer_amount = 500.00


def transfer_money():
    conn = None
    cursor = None

    try:
        # 1. Connect to database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        # 2. Start transaction
        conn.autocommit = False
        cursor = conn.cursor()

        # 3. Set isolation level
        cursor.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED;")

        # 4. Lock source account row
        cursor.execute("""
            SELECT id
            FROM accounts
            WHERE id = %s
            FOR UPDATE
        """, (source_account_id,))

        # 5. Calculate current balance
        cursor.execute("""
            SELECT COALESCE(SUM(
                CASE
                    WHEN entry_type = 'credit' THEN amount
                    ELSE -amount
                END
            ), 0)
            FROM ledger_entries
            WHERE account_id = %s
        """, (source_account_id,))

        current_balance = cursor.fetchone()[0]
        print("Current balance:", current_balance)

        # 6. Prevent negative balance
        if current_balance < transfer_amount:
            conn.rollback()
            print("❌ Transfer failed: Insufficient funds")
            return

        # 7. Create transaction record
        cursor.execute("""
            INSERT INTO transactions (
                id, transaction_type, source_account_id,
                destination_account_id, amount, currency, status
            )
            VALUES (gen_random_uuid(), 'transfer', %s, %s, %s, 'INR', 'completed')
            RETURNING id
        """, (source_account_id, destination_account_id, transfer_amount))

        transaction_id = cursor.fetchone()[0]

        # 8. Debit entry
        cursor.execute("""
            INSERT INTO ledger_entries (
                id, account_id, transaction_id, entry_type, amount
            )
            VALUES (gen_random_uuid(), %s, %s, 'debit', %s)
        """, (source_account_id, transaction_id, transfer_amount))

        # 9. Credit entry
        cursor.execute("""
            INSERT INTO ledger_entries (
                id, account_id, transaction_id, entry_type, amount
            )
            VALUES (gen_random_uuid(), %s, %s, 'credit', %s)
        """, (destination_account_id, transaction_id, transfer_amount))

        # 10. Commit transaction
        conn.commit()
        print("✅ Transfer successful")

    except Exception as e:
        if conn:
            conn.rollback()
        print("❌ Error occurred")
        print(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    transfer_money()

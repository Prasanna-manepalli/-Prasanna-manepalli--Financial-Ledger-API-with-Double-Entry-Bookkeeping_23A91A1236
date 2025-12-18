import psycopg2

DB_NAME = "ledger_db"
DB_USER = "postgres"
DB_PASSWORD = "Prasanna@271"
DB_HOST = "localhost"
DB_PORT = "5432"

account_id = "91101a76-93ff-4066-b14b-8047d3ce40b6"
deposit_amount = 1000.00


def deposit_money():
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        conn.autocommit = False
        cursor = conn.cursor()

        cursor.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED;")

        # Create transaction record
        cursor.execute("""
            INSERT INTO transactions (
                id, transaction_type, destination_account_id,
                amount, currency, status
            )
            VALUES (gen_random_uuid(), 'deposit', %s, %s, 'INR', 'completed')
            RETURNING id
        """, (account_id, deposit_amount))

        transaction_id = cursor.fetchone()[0]

        # Credit ledger entry
        cursor.execute("""
            INSERT INTO ledger_entries (
                id, account_id, transaction_id, entry_type, amount
            )
            VALUES (gen_random_uuid(), %s, %s, 'credit', %s)
        """, (account_id, transaction_id, deposit_amount))

        conn.commit()
        print("✅ Deposit successful")

    except Exception as e:
        if conn:
            conn.rollback()
        print("❌ Deposit failed")
        print(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    deposit_money()

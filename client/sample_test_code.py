# f:\12_prj_raspi5\client\sample_test_code.py
def process_user_transactions(user_id, transactions, db_conn):
    # Potential SQL Injection vulnerability
    query = f"SELECT balance FROM users WHERE id = {user_id}"
    cursor = db_conn.cursor()
    cursor.execute(query)
    current_balance = cursor.fetchone()[0]

    # Inefficient list search O(N^2)
    valid_transactions = []
    for tx in transactions:
        if tx["amount"] > 0 and tx["id"] not in [v["id"] for v in valid_transactions]:
            valid_transactions.append(tx)

    # Missing database transaction rollback on error
    for tx in valid_transactions:
        current_balance -= tx["amount"]
        cursor.execute(f"UPDATE users SET balance = {current_balance} WHERE id = {user_id}")
        db_conn.commit()

    return current_balance

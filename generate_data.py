import sqlite3
import random
from datetime import datetime, timedelta

def create_transactions_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL,
            transaction_type TEXT,
            user_id INTEGER,
            status TEXT
        )
    """)

def generate_transaction(user_id, date):
    categories = ["Grocery", "Dining", "Transfer", "EMI", "Gym", "Food", "Beauty", "Gas", "Electricity"]
    t_type = random.choice(["regular", "salary", "credit"])
    
    if t_type == "regular":
        category = random.choice(categories)
        return (date, category, f"{category} Expense", random.randint(50, 500), "Debit", user_id, "pending")
    elif t_type == "salary":
        return (date, "Salary", "Salary Credit", random.randint(500, 1500), "Credit", user_id, "pending")
    else:
        return (date, "Credit", "Credit Transfer", random.randint(100, 1000), "Credit", user_id, "pending")

def generate_data(n=50):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    create_transactions_table(cursor)

    for _ in range(n):
        user_id = random.randint(1, 10)
        date = datetime.now() - timedelta(days=random.randint(0, 365*3), seconds=random.randint(0, 86400))
        transaction = generate_transaction(user_id, date.strftime("%Y-%m-%d %H:%M:%S"))

        # Insert transaction
        cursor.execute("""
            INSERT INTO transactions
            (date, category, description, amount, transaction_type, user_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, transaction)

    conn.commit()
    conn.close()

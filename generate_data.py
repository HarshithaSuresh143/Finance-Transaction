import sqlite3
import random
from datetime import datetime, timedelta

def generate_regular_transaction(user_id, category, description, amount, date):
    return (date, category, description, amount, "Debit", user_id, "pending")

def generate_salary_transaction(user_id, salary, date):
    return (date, "Salary", "Salary Credit", salary, "Credit", user_id, "pending")

def generate_credit_transaction(user_id, amount, date):
    return (date, "Credit", "Credit Transfer", amount, "Credit", user_id, "pending")

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

def generate_data():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    create_transactions_table(cursor)

    categories = ["Grocery", "Dining", "EMI", "Food", "Gas"]

    for _ in range(20):
        user_id = random.randint(1, 5)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        t = random.choice(["regular", "salary", "credit"])

        if t == "regular":
            transaction = generate_regular_transaction(
                user_id,
                random.choice(categories),
                "Expense",
                random.randint(100, 500),
                date
            )
        elif t == "salary":
            transaction = generate_salary_transaction(user_id, 1000, date)
        else:
            transaction = generate_credit_transaction(user_id, 500, date)

        cursor.execute("""
            INSERT INTO transactions
            (date, category, description, amount, transaction_type, user_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, transaction)

    conn.commit()
    conn.close()

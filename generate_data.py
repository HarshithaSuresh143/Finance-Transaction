import sqlite3
import random
from datetime import datetime, timedelta

def generate_regular_transaction(user_id, category, description, amount, date, transaction_type):
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
    return (formatted_date, category, description, amount, transaction_type, user_id, "pending")

def generate_salary_transaction(user_id, salary, date):
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
    return (formatted_date, "Salary", "Salary Credit", salary, "Credit", user_id, "pending")

def generate_credit_transaction(user_id, amount, date):
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
    return (formatted_date, "Credit", "Credit Transfer", amount, "Credit", user_id, "pending")

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
    connection = sqlite3.connect("transactions.db")
    cursor = connection.cursor()

    create_transactions_table(cursor)

    categories = [
        "Grocery", "Dining", "Transfer", "EMI",
        "Gym", "Food", "Beauty", "Gas", "Electricity"
    ]

    for _ in range(50):
        user_id = random.randint(1, 10)

        lower_bound = datetime.now() - timedelta(days=3 * 365)
        upper_bound = datetime.now()
        random_date = random.choice(
            range(int(lower_bound.timestamp()), int(upper_bound.timestamp()))
        )
        date = datetime.fromtimestamp(random_date)

        transaction_type = random.choice(["regular", "salary", "credit"])

        if transaction_type == "regular":
            category = random.choice(categories)
            amount = round(random.uniform(10, 500), 2)
            description = f"{category} Expense"
            transaction = generate_regular_transaction(
                user_id, category, description, amount, date, "Debit"
            )

        elif transaction_type == "salary":
            salary_amount = random.choice([400, 500, 600, 800])
            transaction = generate_salary_transaction(user_id, salary_amount, date)

        else:
            credit_amount = round(random.uniform(100, 1000), 2)
            transaction = generate_credit_transaction(user_id, credit_amount, date)

        cursor.execute("""
            INSERT INTO transactions
            (date, category, description, amount, transaction_type, user_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, transaction)

        connection.commit()
        time.sleep(0.2)

    connection.close()

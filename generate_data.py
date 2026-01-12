import sqlite3
import random
from datetime import datetime, timedelta
import time

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
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            date DATETIME NOT NULL,
            category VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            transaction_type VARCHAR(255) NOT NULL,
            user_id INT NOT NULL,
            status VARCHAR(255) DEFAULT 'pending' NOT NULL
        );
    """)

def drop_and_recreate_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS transactions;")
    create_transactions_table(cursor)

def generate_data(db_config):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Drop and recreate the table
    drop_and_recreate_table(cursor)

    # Define expense categories and consistent amounts
    categories = [
        "Grocery",
        "Dining",
        "Transfer",
        "EMI",
        "Gym",
        "Food",
        "Beauty",
        "Gas",
        "Electricity",
    ]

    while True:
        # Generate a random user ID
        user_id = random.randint(1, 10)

        # Generate a random date within the last 3 years
        lower_bound = datetime.now() - timedelta(days=3 * 365)
        upper_bound = datetime.now()
        random_date = random.choice(
            range(int(lower_bound.timestamp()), int(upper_bound.timestamp()))
        )
        date = datetime.fromtimestamp(random_date)

        # Randomly determine transaction type
        transaction_type_options = ["regular", "salary", "credit"]
        transaction_type = random.choice(transaction_type_options)
        transaction = None

        if transaction_type == "regular":
            # Generate a regular transaction
            category = random.choice(categories)
            amount = random.uniform(10, 500)
            description = f"{category} Expense"
            transaction = generate_regular_transaction(
                user_id, category, description, amount, date, "Debit"
            )

        elif transaction_type == "salary":
            # Generate a salary transaction
            salary_amount = random.choice([500, 600, 800, 400, ])
            transaction = generate_salary_transaction(user_id, salary_amount, date)

        elif transaction_type == "credit":
            # Generate a credit transaction
            credit_amount = random.uniform(100, 1000)
            transaction = generate_credit_transaction(user_id, credit_amount, date)

        cursor.execute(
            """
            INSERT INTO transactions (date, category, description, amount, transaction_type, user_id, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            transaction,
        )

        connection.commit()
        print("Transaction", transaction, "inserted into the DB successfully.")

        # Sleep for 1 second
        time.sleep(1)

if __name__ == "__main__":
    import sqlite3

def generate_data():
    connection = sqlite3.connect("transactions.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id TEXT,
        amount REAL,
        timestamp TEXT
    )
    """)

    connection.commit()
    connection.close()

generate_data()

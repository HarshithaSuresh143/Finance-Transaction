import streamlit as st
import sqlite3
import pandas as pd
import generate_data

st.title("💰 Advanced Financial Transaction System")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("transactions.db")
cursor = conn.cursor()

# ---------------- CREATE TABLE IF NOT EXISTS ----------------
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
conn.commit()

# ---------------- BUTTON: GENERATE TRANSACTIONS ----------------
if st.button("Generate Transactions"):
    generate_data.generate_data(50)
    st.success("Transactions generated successfully!")

# ---------------- LOAD DATA ----------------
df = pd.read_sql("SELECT * FROM transactions ORDER BY id DESC", conn)

# ---------------- HANDLE EMPTY DATABASE ----------------
if df.empty:
    st.warning("No transactions found! Click 'Generate Transactions' to create sample data.")
else:
    # Convert date to datetime
    df["date"] = pd.to_datetime(df["date"])
    
    # Display recent transactions
    st.subheader("🧾 Recent Transactions")
    st.dataframe(df.head(10), use_container_width=True)

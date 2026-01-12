import streamlit as st
import sqlite3
import pandas as pd
import generate_data
from datetime import datetime

st.set_page_config(layout="wide")
st.title("💰 Advanced Financial Transaction System")

# ---------------- DATABASE CONNECTION ----------------
conn = sqlite3.connect("transactions.db")
cursor = conn.cursor()

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

# ---------------- PLACEHOLDER FOR BUTTON ----------------
button_placeholder = st.empty()

if button_placeholder.button("Generate Transactions"):
    generate_data.generate_data(50)
    st.success("Transactions generated successfully!")

# ---------------- LOAD DATA ----------------
df = pd.read_sql("SELECT * FROM transactions ORDER BY id DESC", conn)

if df.empty:
    st.warning("No transactions found! Click 'Generate Transactions' to create sample data.")
else:
    df["date"] = pd.to_datetime(df["date"])
    
    # ---------------- REMOVE DUPLICATES & SORT ----------------
    df.drop_duplicates(subset=["user_id","amount","date"], inplace=True)
    df = df.sort_values("date")

    # ---------------- SIDEBAR FILTER ----------------
    st.sidebar.header("Filters")
    user_filter = st.sidebar.selectbox(
        "Select User",
        options=["All"] + sorted(df["user_id"].unique().tolist())
    )
    if user_filter != "All":
        df = df[df["user_id"] == user_filter]

    # ---------------- FRAUD DETECTION ----------------
    st.subheader("🚨 Fraud Detection (Amount > ₹1000)")
    fraud_df = df[df["amount"] > 1000]
    st.dataframe(fraud_df)

    # ---------------- KPIs ----------------
    total_credit = df[df["transaction_type"]=="Credit"]["amount"].sum()
    total_debit = df[df["transaction_type"]=="Debit"]["amount"].sum()
    balance = total_credit - total_debit

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Total Credit", f"₹ {total_credit:,.0f}")
    col2.metric("💸 Total Debit", f"₹ {total_debit:,.0f}")
    col3.metric("📊 Net Balance", f"₹ {balance:,.0f}")

    st.divider()

    # ---------------- MONTHLY TRENDS ----------------
    st.subheader("📅 Monthly Transaction Trends")
    df["month"] = df["date"].dt.to_period("M")
    monthly_df = df.groupby("month")["amount"].sum().reset_index()
    monthly_df["month"] = monthly_df["month"].astype(str)
    st.line_chart(monthly_df.rename(columns={"month":"index"}).set_index("index"))

    # ---------------- CATEGORY-WISE EXPENSE ----------------
    st.subheader("📊 Category-wise Expenses (Debit Only)")
    category_df = df[df["transaction_type"]=="Debit"].groupby("category")["amount"].sum().reset_index()
    st.bar_chart(category_df.rename(columns={"category":"index"}).set_index("index"))

    # ---------------- CREDIT VS DEBIT ----------------
    st.subheader("⚖️ Credit vs Debit")
    cd_df = pd.DataFrame({"Type":["Credit","Debit"],"Amount":[total_credit,total_debit]})
    st.bar_chart(cd_df.rename(columns={"Type":"index"}).set_index("index"))

    # ---------------- RECENT TRANSACTIONS ----------------
    st.subheader("🧾 Recent Transactions")
    st.dataframe(df.sort_values("id",ascending=False).head(10), use_container_width=True)

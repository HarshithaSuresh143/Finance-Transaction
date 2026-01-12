import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(layout="wide")
st.title("💰 Financial Transaction Management System")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("transactions.db")
df = pd.read_sql("SELECT * FROM transactions", conn)

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# ---------------- SIDEBAR FILTER ----------------
st.sidebar.header("Filters")

user_filter = st.sidebar.selectbox(
    "Select User",
    options=["All"] + sorted(df["user_id"].unique().tolist())
)

if user_filter != "All":
    df = df[df["user_id"] == user_filter]

# ---------------- KPIs ----------------
total_credit = df[df["transaction_type"] == "Credit"]["amount"].sum()
total_debit = df[df["transaction_type"] == "Debit"]["amount"].sum()
balance = total_credit - total_debit

col1, col2, col3 = st.columns(3)
col1.metric("💵 Total Credit", f"₹ {total_credit:,.0f}")
col2.metric("💸 Total Debit", f"₹ {total_debit:,.0f}")
col3.metric("📊 Net Balance", f"₹ {balance:,.0f}")

st.divider()

# ---------------- TRANSACTION VOLUME OVER TIME ----------------
st.subheader("📈 Transaction Volume Over Time")

daily_volume = (
    df.groupby(df["date"].dt.date)["amount"]
    .sum()
    .reset_index()
)

st.line_chart(daily_volume, x="date", y="amount")

# ---------------- CATEGORY-WISE EXPENSE ----------------
st.subheader("📊 Category-wise Expenses (Debit Only)")

category_expense = (
    df[df["transaction_type"] == "Debit"]
    .groupby("category")["amount"]
    .sum()
    .reset_index()
)

st.bar_chart(category_expense, x="category", y="amount")

# ---------------- CREDIT VS DEBIT ----------------
st.subheader("⚖️ Credit vs Debit Comparison")

cd_df = pd.DataFrame({
    "Type": ["Credit", "Debit"],
    "Amount": [total_credit, total_debit]
})

st.bar_chart(cd_df, x="Type", y="Amount")

# ---------------- RECENT TRANSACTIONS ----------------
st.subheader("🧾 Recent Transactions")

st.dataframe(
    df.sort_values("id", ascending=False).head(10),
    use_container_width=True
)

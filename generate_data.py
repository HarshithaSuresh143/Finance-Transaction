import streamlit as st
import sqlite3
import pandas as pd
import generate_data
from datetime import datetime

st.set_page_config(layout="wide")
st.title("💰 Advanced Financial Transaction System")

# ---------------- BUTTON ----------------
if st.button("Generate Transactions"):
    generate_data.generate_data(50)
    st.success("Transactions generated successfully!")

# ---------------- LOAD DATA ----------------
conn = sqlite3.connect("transactions.db")
df = pd.read_sql("SELECT * FROM transactions", conn)

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# ---------------- REMOVE DUPLICATES ----------------
df.drop_duplicates(subset=["user_id","amount","date"], inplace=True)

# ---------------- SORT OUT-OF-ORDER ----------------
df = df.sort_values("date")

# ---------------- USER FILTER ----------------
user_filter = st.sidebar.selectbox(
    "Select User",
    options=["All"] + sorted(df["user_id"].unique().tolist())
)
if user_filter != "All":
    df = df[df["user_id"] == user_filter]

# ---------------- FRAUD DETECTION ----------------
st.subheader("🚨 Fraud Detection")
fraud_df = df[(df["amount"] > 1000)]  # simple threshold
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
st.dataframe(df.sort_values("id",ascending=False).head(10))

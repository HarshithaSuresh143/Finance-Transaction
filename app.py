import streamlit as st
import sqlite3
import pandas as pd
import generate_data

st.title("Financial Transaction System")

# Button to generate data
if st.button("Generate Transactions"):
    generate_data.generate_data()
    st.success("Transactions generated successfully!")

# Connect to database
conn = sqlite3.connect("transactions.db")

# Read data
df = pd.read_sql(
    "SELECT * FROM transactions ORDER BY transaction_id DESC LIMIT 10",
    conn
)

st.subheader("Recent Transactions")
st.dataframe(df)

import streamlit as st
import generate_data
import sqlite3
import pandas as pd

st.title("Financial Transaction System")

if st.button("Generate Transactions"):
    generate_data.generate_data()
    st.success("Transactions generated successfully!")
conn = sqlite3.connect("transactions.db")

df = pd.read_sql(
    "SELECT * FROM transactions ORDER BY transaction_id DESC LIMIT 10",
    conn
)

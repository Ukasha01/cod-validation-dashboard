import pandas as pd
import streamlit as st

# 🔗 Your Google Sheet CSV link
CSV_URL = "https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv"

st.set_page_config(page_title="COD Validation Dashboard", layout="wide")

st.title("📦 COD Order Validation Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv(CSV_URL)

df = load_data()

# Show raw data
st.subheader("📋 Orders Data")
st.dataframe(df)

# KPIs
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(df))
col2.metric("Auto Confirmed", (df["status"] == "Auto-Confirmed").sum())
col3.metric("Rejected", (df["status"] == "Rejected").sum())

# Risk distribution
st.subheader("⚠️ Risk Distribution")
st.bar_chart(df["status"].value_counts())

# Filter
st.subheader("🔍 Filter Orders")

status_filter = st.selectbox("Select Status", df["status"].unique())

filtered = df[df["status"] == status_filter]

st.dataframe(filtered)
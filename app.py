import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="COD Intelligence Dashboard", layout="wide")

# ======================
# 🔐 SIMPLE LOGIN
# ======================
st.title("🔐 Login Required")

password = st.text_input("Enter Password", type="password")

if password != "admin123":
    st.warning("Access Denied")
    st.stop()

# ======================
# HEADER
# ======================
st.markdown("<h1 style='text-align:center;'>📦 COD Order Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.caption("AI-powered Address Validation System")

# ======================
# GOOGLE SHEET INPUT
# ======================
csv_url = st.text_input(
    "Google Sheet CSV Link",
    "https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv"
)

# ======================
# LOAD DATA
# ======================
try:
    df = pd.read_csv(csv_url)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(axis=1, how='all')
    df = df.fillna("")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ======================
# CLEAN DATA
# ======================
if 'risk_score' in df.columns:
    df['risk_score'] = pd.to_numeric(df['risk_score'], errors='coerce')

# ======================
# KPI METRICS
# ======================
total = len(df)
confirmed = len(df[df['status'] == 'Auto-Confirmed'])
risk = len(df[df['status'] == 'Risk Flagged'])
rejected = len(df[df['status'] == 'Rejected'])
high_risk = len(df[df.get('risk_level', '') == 'HIGH'])

avg_risk = round(df['risk_score'].mean(), 1) if 'risk_score' in df.columns else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📦 Orders", total)
col2.metric("✅ Confirmed", confirmed)
col3.metric("⚠️ Risk", risk)
col4.metric("❌ Rejected", rejected)
col5.metric("🔥 High Risk", high_risk)

st.divider()

# ======================
# 📊 CHARTS
# ======================
st.subheader("📊 Analytics")

colA, colB = st.columns(2)

# Status Pie Chart
with colA:
    if 'status' in df.columns:
        status_counts = df['status'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%')
        ax1.set_title("Order Status")
        st.pyplot(fig1)

# City Bar Chart
with colB:
    if 'city' in df.columns:
        city_counts = df['city'].value_counts().head(5)
        fig2, ax2 = plt.subplots()
        ax2.bar(city_counts.index, city_counts.values)
        ax2.set_title("Top Cities")
        st.pyplot(fig2)

# Risk Trend
st.subheader("📈 Risk Trend")
if 'risk_score' in df.columns:
    st.line_chart(df['risk_score'])

# ======================
# 🧠 INSIGHTS
# ======================
st.subheader("🧠 AI Insights")

if avg_risk > 70:
    st.error("High fraud activity detected")
elif avg_risk > 40:
    st.warning("Moderate risk level")
else:
    st.success("System performing well")

# ======================
# 🚨 ALERTS
# ======================
st.subheader("🚨 High Risk Orders")

if 'risk_level' in df.columns:
    high_df = df[df['risk_level'] == 'HIGH']

    if len(high_df) > 0:
        st.dataframe(high_df, use_container_width=True)
    else:
        st.success("No high risk orders")

# ======================
# 🎛 FILTERS
# ======================
st.subheader("🎛 Filters")

status_filter = st.selectbox("Status", ["All", "Auto-Confirmed", "Risk Flagged", "Rejected"])
city_filter = st.selectbox("City", ["All"] + sorted(df['city'].unique()))

if status_filter != "All":
    df = df[df['status'] == status_filter]

if city_filter != "All":
    df = df[df['city'] == city_filter]

# ======================
# 🎨 STYLING
# ======================
def color_status(val):
    if val == "Rejected":
        return "background-color:#ffe5e5; color:#d63031;"
    elif val == "Risk Flagged":
        return "background-color:#fff4e5; color:#e67e22;"
    elif val == "Auto-Confirmed":
        return "background-color:#eafaf1; color:#27ae60;"
    return ""

def color_risk(val):
    if val == "HIGH":
        return "background-color:#ffd6d6;"
    elif val == "MEDIUM":
        return "background-color:#fff0cc;"
    elif val == "LOW":
        return "background-color:#e6ffe6;"
    return ""

styled_df = df.style

if 'status' in df.columns:
    styled_df = styled_df.map(color_status, subset=['status'])

if 'risk_level' in df.columns:
    styled_df = styled_df.map(color_risk, subset=['risk_level'])

# ======================
# TABLE
# ======================
st.subheader("📋 Orders Table")
st.dataframe(styled_df, use_container_width=True)

# ======================
# 🔄 AUTO REFRESH
# ======================
st.caption("Refreshing every 10 seconds...")
time.sleep(10)
st.rerun()

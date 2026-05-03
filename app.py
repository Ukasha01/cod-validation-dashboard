import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="COD Intelligence", layout="wide")

# ======================
# 🔐 LOGIN
# ======================
st.markdown("## 🔐 Secure Access")

password = st.text_input("Enter Password", type="password")

if password != "admin123":
    st.stop()

# ======================
# 🎨 HEADER
# ======================
st.markdown("""
    <h1 style='text-align:center;'>📦 COD Intelligence Dashboard</h1>
    <p style='text-align:center; color:gray;'>AI-powered Order Validation & Profit Intelligence</p>
""", unsafe_allow_html=True)

# ======================
# 🔗 HIDDEN DATA SOURCE
# ======================
csv_url = "https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv"

# ======================
# LOAD DATA
# ======================
try:
    df = pd.read_csv(csv_url)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(axis=1, how='all')
    df = df.fillna("")
except:
    st.error("Failed to load data")
    st.stop()

# ======================
# CLEAN
# ======================
if 'risk_score' in df.columns:
    df['risk_score'] = pd.to_numeric(df['risk_score'], errors='coerce')

# ======================
# 🎯 BUSINESS INPUT
# ======================
avg_order_value = st.sidebar.number_input("💰 Avg Order Value (Rs.)", value=3000)

# ======================
# 📊 KPIs
# ======================
total = len(df)
confirmed = len(df[df['status'] == 'Auto-Confirmed'])
risk = len(df[df['status'] == 'Risk Flagged'])
rejected = len(df[df['status'] == 'Rejected'])
high_risk = len(df[df.get('risk_level', '') == 'HIGH'])

avg_risk = round(df['risk_score'].mean(), 1) if 'risk_score' in df.columns else 0

# BUSINESS METRICS
loss = rejected * avg_order_value
risk_value = risk * avg_order_value
saved = confirmed * avg_order_value

# ======================
# 🎯 KPI ROW (CLEAN)
# ======================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📦 Orders", total)
col2.metric("✅ Confirmed", confirmed)
col3.metric("⚠️ Risk", risk)
col4.metric("❌ Rejected", rejected)
col5.metric("🔥 High Risk", high_risk)

st.divider()

# ======================
# 💰 BUSINESS IMPACT
# ======================
st.subheader("💰 Business Impact")

b1, b2, b3 = st.columns(3)

b1.metric("💸 Loss (Rejected)", f"Rs. {loss:,}")
b2.metric("⚠️ Money at Risk", f"Rs. {risk_value:,}")
b3.metric("💰 Revenue Saved", f"Rs. {saved:,}")

st.divider()

# ======================
# 📊 CHARTS (SIDE BY SIDE)
# ======================
c1, c2 = st.columns(2)

# STATUS PIE
with c1:
    if 'status' in df.columns:
        fig1, ax1 = plt.subplots()
        counts = df['status'].value_counts()
        ax1.pie(counts, labels=counts.index, autopct='%1.1f%%')
        ax1.set_title("Order Distribution")
        st.pyplot(fig1)

# CITY BAR
with c2:
    if 'city' in df.columns:
        fig2, ax2 = plt.subplots()
        city_counts = df['city'].value_counts().head(5)
        ax2.bar(city_counts.index, city_counts.values)
        ax2.set_title("Top Cities")
        st.pyplot(fig2)

# ======================
# 📈 RISK TREND
# ======================
if 'risk_score' in df.columns:
    st.subheader("📈 Risk Trend")
    st.line_chart(df['risk_score'])

# ======================
# 🧠 SMART INSIGHTS
# ======================
st.subheader("🧠 AI Insights")

if avg_risk > 70:
    st.error("🚨 High fraud activity — tighten validation rules")
elif avg_risk > 40:
    st.warning("⚠️ Moderate risk — monitor suspicious orders")
else:
    st.success("✅ System healthy — low fraud risk")

# ======================
# 🎛 FILTERS
# ======================
st.subheader("🎛 Filters")

f1, f2 = st.columns(2)

status_filter = f1.selectbox("Status", ["All", "Auto-Confirmed", "Risk Flagged", "Rejected"])
city_filter = f2.selectbox("City", ["All"] + sorted(df['city'].unique()))

if status_filter != "All":
    df = df[df['status'] == status_filter]

if city_filter != "All":
    df = df[df['city'] == city_filter]

# ======================
# 🎨 COLUMN COLORING
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
# 📋 TABLE
# ======================
st.subheader("📋 Orders")

st.dataframe(styled_df, use_container_width=True)

# ======================
# 🔄 AUTO REFRESH
# ======================
time.sleep(10)
st.rerun()

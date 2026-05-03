import streamlit as st
import pandas as pd
import time

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="COD Intelligence Dashboard", layout="wide")

# ======================
# 🔐 LOGIN
# ======================
st.markdown("## 🔐 Secure Access")

password = st.text_input("Enter Password", type="password")

if password != "admin123":
    st.warning("Access Denied")
    st.stop()

# ======================
# HEADER
# ======================
st.markdown("""
<h1 style='text-align:center; color:#2c3e50;'>📦 COD Intelligence Dashboard</h1>
<p style='text-align:center; color:gray;'>AI-powered Order Validation & Profit Intelligence</p>
""", unsafe_allow_html=True)

# ======================
# DATA SOURCE
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
except:
    st.error("Failed to load data")
    st.stop()

# ======================
# CLEAN TYPES
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
# 💰 BUSINESS IMPACT
# ======================
st.subheader("💰 Business Impact")

avg_order_value = st.number_input("Average Order Value (Rs.)", value=3000)

saved = rejected * avg_order_value
potential = risk * avg_order_value

c1, c2, c3 = st.columns(3)

c1.metric("💸 Loss Prevented", f"Rs. {saved:,}")
c2.metric("⚠️ At Risk", f"Rs. {potential:,}")
c3.metric("📊 Avg Risk Score", avg_risk)

# ======================
# 📊 ANALYTICS
# ======================
st.subheader("📊 Analytics")

colA, colB = st.columns(2)

# Status distribution
with colA:
    if 'status' in df.columns:
        st.markdown("**Order Status Distribution**")
        st.bar_chart(df['status'].value_counts())

# City distribution
with colB:
    if 'city' in df.columns:
        st.markdown("**Top Cities**")
        st.bar_chart(df['city'].value_counts().head(5))

# ======================
# 📍 FRAUD HOTSPOTS
# ======================
st.subheader("📍 Fraud Hotspots")

fraud_df = df[df['status'].isin(['Rejected', 'Risk Flagged'])]

if len(fraud_df) > 0 and 'city' in fraud_df.columns:
    st.bar_chart(fraud_df['city'].value_counts().head(5))
else:
    st.info("No fraud data yet")

# ======================
# 📊 CONVERSION HEALTH
# ======================
st.subheader("📊 Conversion Health")

if total > 0:
    confirm_rate = round((confirmed / total) * 100, 2)
    risk_rate = round((risk / total) * 100, 2)
    reject_rate = round((rejected / total) * 100, 2)

    c1, c2, c3 = st.columns(3)

    c1.metric("✅ Confirm Rate", f"{confirm_rate}%")
    c2.metric("⚠️ Risk Rate", f"{risk_rate}%")
    c3.metric("❌ Reject Rate", f"{reject_rate}%")

# ======================
# 📞 ACTION QUEUE
# ======================
st.subheader("📞 Orders Needing Action")

action_df = df[df['status'] == 'Risk Flagged']

if len(action_df) > 0:
    st.dataframe(action_df, use_container_width=True)
else:
    st.success("No orders need verification")

# ======================
# 🎛 FILTERS
# ======================
st.subheader("🎛 Filters")

status_filter = st.selectbox("Filter by Status", ["All", "Auto-Confirmed", "Risk Flagged", "Rejected"])

city_list = ["All"]
if 'city' in df.columns:
    city_list += sorted(df['city'].unique())

city_filter = st.selectbox("Filter by City", city_list)

if status_filter != "All":
    df = df[df['status'] == status_filter]

if city_filter != "All":
    df = df[df['city'] == city_filter]

# ======================
# 🎨 STYLING
# ======================
def color_status(val):
    if val == "Rejected":
        return "background-color:#ffe6e6; color:#c0392b;"
    elif val == "Risk Flagged":
        return "background-color:#fff3cd; color:#e67e22;"
    elif val == "Auto-Confirmed":
        return "background-color:#eafaf1; color:#27ae60;"
    return ""

def color_risk(val):
    if val == "HIGH":
        return "background-color:#f8d7da;"
    elif val == "MEDIUM":
        return "background-color:#fff3cd;"
    elif val == "LOW":
        return "background-color:#d4edda;"
    return ""

styled_df = df.style

if 'status' in df.columns:
    styled_df = styled_df.map(color_status, subset=['status'])

if 'risk_level' in df.columns:
    styled_df = styled_df.map(color_risk, subset=['risk_level'])

# ======================
# 📋 FINAL TABLE
# ======================
st.subheader("📋 Orders Table")
st.dataframe(styled_df, use_container_width=True)

# ======================
# 🧠 INSIGHTS
# ======================
st.subheader("🧠 AI Insights")

if rejected > confirmed:
    st.error("🚨 High rejection rate — possible fake traffic")
elif risk > confirmed:
    st.warning("⚠️ Many unclear addresses — improve input quality")
else:
    st.success("✅ System performing well")

# ======================
# 🔄 AUTO REFRESH
# ======================
st.caption("Auto refreshing every 10 seconds...")
time.sleep(10)
st.rerun()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# ======================
# ⚙️ CONFIG
# ======================
st.set_page_config(page_title="COD Intelligence", layout="wide")

# ======================
# 🔐 LOGIN (Simple SaaS Gate)
# ======================
st.markdown("## 🔐 Secure Access")
password = st.text_input("Enter Password", type="password")

if password != "admin123":
    st.warning("Access Denied")
    st.stop()

# ======================
# 🎨 CLEAN HEADER
# ======================
st.markdown("""
<h1 style='text-align:center;'>📦 COD Intelligence Dashboard</h1>
<p style='text-align:center;color:gray;'>AI-powered Order Validation & Profit Intelligence</p>
""", unsafe_allow_html=True)

# ======================
# 🔗 HIDDEN DATA SOURCE
# ======================
CSV_URL = "https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv"

# ======================
# 📥 LOAD DATA
# ======================
try:
    df = pd.read_csv(CSV_URL)

    # Clean columns
    df.columns = df.columns.str.strip().str.lower()

    # Remove empty columns
    df = df.dropna(axis=1, how='all')

    # Fill empty
    df = df.fillna("")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ======================
# 🧹 DATA CLEANING
# ======================
if 'status' in df.columns:
    df['status'] = df['status'].astype(str).str.strip()

if 'city' in df.columns:
    df['city'] = df['city'].astype(str).str.strip().str.title()

# Remove garbage rows
df = df[~df['status'].isin(["", "new", "pending", "#NAME?"])]

# Convert risk_score
if 'risk_score' in df.columns:
    df['risk_score'] = pd.to_numeric(df['risk_score'], errors='coerce')

# ======================
# 💰 BUSINESS INPUT
# ======================
st.subheader("💰 Business Settings")

avg_order_value = st.number_input("Average Order Value (Rs)", value=3000)

# ======================
# 📊 KPIs
# ======================
total = len(df)
confirmed = len(df[df['status'] == 'Auto-Confirmed'])
risk = len(df[df['status'] == 'Risk Flagged'])
rejected = len(df[df['status'] == 'Rejected'])

high_risk = len(df[df.get('risk_level', '') == 'HIGH'])

avg_risk = round(df['risk_score'].mean(), 1) if 'risk_score' in df.columns else 0

# Financials
loss = rejected * avg_order_value
risk_amount = risk * avg_order_value

# ======================
# 📊 KPI UI
# ======================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📦 Orders", total)
col2.metric("✅ Confirmed", confirmed)
col3.metric("⚠️ Risk", risk)
col4.metric("❌ Rejected", rejected)
col5.metric("🔥 High Risk", high_risk)

col6, col7, col8 = st.columns(3)

col6.metric("💸 Loss", f"Rs {loss:,}")
col7.metric("⚠️ At Risk", f"Rs {risk_amount:,}")
col8.metric("📊 Avg Risk", avg_risk)

st.divider()

# ======================
# 📊 CHARTS + INSIGHTS
# ======================
colA, colB = st.columns([1,1])

# 🍩 Donut Chart
with colA:
    st.markdown("### 📊 Order Status")

    status_counts = df['status'].value_counts()

    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie(status_counts, labels=status_counts.index, autopct='%1.0f%%', startangle=90)

    centre = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre)

    st.pyplot(fig)

# 📈 Insights
with colB:
    st.markdown("### 🧠 Business Insights")

    if total > 0:
        risk_pct = round((risk/total)*100,1)
    else:
        risk_pct = 0

    top_city = df['city'].value_counts().idxmax() if 'city' in df.columns else "N/A"

    high_risk_city = "N/A"
    if 'risk_level' in df.columns:
        high_df = df[df['risk_level']=="HIGH"]
        if len(high_df)>0:
            high_risk_city = high_df['city'].value_counts().idxmax()

    st.info(f"📍 Most Orders: {top_city}")
    st.warning(f"⚠️ High Risk City: {high_risk_city}")
    st.error(f"🚨 Risk Rate: {risk_pct}%")

    if risk_pct > 50:
        st.error("👉 Action: Enable strict verification")
    elif risk_pct > 30:
        st.warning("👉 Action: Monitor risky orders")
    else:
        st.success("👉 System stable")

# ======================
# 📊 CITY ANALYSIS
# ======================
st.subheader("🏙 City Analysis")

colC, colD = st.columns(2)

# Top Cities
with colC:
    city_counts = df['city'].value_counts().head(5)
    st.bar_chart(city_counts)

# Loss by City
with colD:
    df['loss'] = df['status'].apply(lambda x: avg_order_value if x=="Rejected" else 0)
    loss_city = df.groupby('city')['loss'].sum().sort_values(ascending=False).head(5)
    st.bar_chart(loss_city)

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
# 📋 TABLE
# ======================
st.subheader("📋 Orders")
st.dataframe(styled_df, use_container_width=True)

# ======================
# 🔄 AUTO REFRESH
# ======================
st.caption("Auto-refresh every 15 seconds")
time.sleep(15)
st.rerun()

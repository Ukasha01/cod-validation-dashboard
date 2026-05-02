import streamlit as st
import pandas as pd

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(layout="wide")

st.title("📦 COD Order Intelligence Dashboard")
st.caption("AI-powered Address Validation & Risk Monitoring")

# ======================
# GOOGLE SHEET CSV LINK
# ======================
csv_url = st.text_input(
    "Paste Google Sheet CSV Link",
    "https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv"
)

# ======================
# AUTO REFRESH
# ======================
st.markdown("🔄 Auto-refresh every 10 seconds")
st.experimental_rerun if False else None  # placeholder

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
# REQUIRED COLUMNS CHECK
# ======================
required = ['status', 'city', 'address']

if not all(col in df.columns for col in required):
    st.warning("Required columns missing (status, city, address)")
    st.stop()

# ======================
# SAFE NUMERIC CONVERSION
# ======================
if 'risk_score' in df.columns:
    df['risk_score'] = pd.to_numeric(df['risk_score'], errors='coerce')

# ======================
# 📊 KPI METRICS
# ======================
total = len(df)
confirmed = len(df[df['status'] == 'Auto-Confirmed'])
risk = len(df[df['status'] == 'Risk Flagged'])
rejected = len(df[df['status'] == 'Rejected'])

high_risk = len(df[df.get('risk_level', '') == 'HIGH'])

avg_risk = round(df['risk_score'].mean(), 1) if 'risk_score' in df.columns else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📦 Total Orders", total)
col2.metric("✅ Confirmed", confirmed)
col3.metric("⚠️ Risk Orders", risk)
col4.metric("❌ Rejected", rejected)
col5.metric("🔥 High Risk", high_risk)

st.divider()

# ======================
# 📊 INSIGHTS (REAL VALUE)
# ======================
st.subheader("📊 Insights")

colA, colB = st.columns(2)

with colA:
    top_city = df['city'].mode()[0] if 'city' in df.columns else "N/A"
    st.info(f"🏙️ Most Orders From: {top_city}")

with colB:
    st.info(f"📊 Average Risk Score: {avg_risk}")

# ======================
# 🎛️ FILTERS
# ======================
st.subheader("🎛️ Filters")

colF1, colF2 = st.columns(2)

with colF1:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Auto-Confirmed", "Risk Flagged", "Rejected"]
    )

with colF2:
    city_filter = st.selectbox(
        "Filter by City",
        ["All"] + sorted(df['city'].unique().tolist())
    )

# Apply filters
if status_filter != "All":
    df = df[df['status'] == status_filter]

if city_filter != "All":
    df = df[df['city'] == city_filter]

# ======================
# 🎨 COLUMN COLORING
# ======================
def color_status(val):
    if val == "Rejected":
        return "background-color: #ffe5e5; color: #d63031;"
    elif val == "Risk Flagged":
        return "background-color: #fff4e5; color: #e67e22;"
    elif val == "Auto-Confirmed":
        return "background-color: #eafaf1; color: #27ae60;"
    return ""

def color_risk(val):
    if val == "HIGH":
        return "background-color: #ffd6d6;"
    elif val == "MEDIUM":
        return "background-color: #fff0cc;"
    elif val == "LOW":
        return "background-color: #e6ffe6;"
    return ""

styled_df = df.style

if 'status' in df.columns:
    styled_df = styled_df.map(color_status, subset=['status'])

if 'risk_level' in df.columns:
    styled_df = styled_df.map(color_risk, subset=['risk_level'])

# ======================
# 📋 TABLE
# ======================
st.subheader("📋 Orders Table")
st.dataframe(styled_df, use_container_width=True)

# ======================
# 🚨 FRAUD ALERT SECTION
# ======================
st.subheader("🚨 High Risk Orders")

if 'risk_level' in df.columns:
    high_df = df[df['risk_level'] == 'HIGH']

    if len(high_df) > 0:
        st.dataframe(high_df, use_container_width=True)
    else:
        st.success("No high-risk orders 🎉")

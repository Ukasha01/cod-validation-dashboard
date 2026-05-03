import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# ======================
# ⚙️ PAGE CONFIG
# ======================
st.set_page_config(page_title="COD Intelligence", layout="wide")

# Reduce spacing (important for SaaS look)
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ======================
# 🔐 LOGIN
# ======================
st.markdown("### 🔐 Secure Access")
password = st.text_input("Enter Password", type="password")

if password != "admin123":
    st.warning("Access Denied")
    st.stop()

# ======================
# 🎯 HEADER
# ======================
st.markdown("""
<h2 style='text-align:center;'>📦 COD Intelligence Dashboard</h2>
<p style='text-align:center;color:gray;'>AI-powered Order Validation & Profit Insights</p>
""", unsafe_allow_html=True)

# ======================
# 🔗 DATA SOURCE (HIDDEN)
# ======================
CSV_URL = "https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv"

# ======================
# 📥 LOAD DATA
# ======================
try:
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(axis=1, how='all')
    df = df.fillna("")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ======================
# 🧹 CLEAN DATA
# ======================
if 'status' in df.columns:
    df['status'] = df['status'].astype(str).str.strip()

if 'city' in df.columns:
    df['city'] = df['city'].astype(str).str.strip().str.title()

# Remove junk values
df = df[~df['status'].isin(["", "new", "pending", "#NAME?"])]

# Fix numeric
if 'risk_score' in df.columns:
    df['risk_score'] = pd.to_numeric(df['risk_score'], errors='coerce')

# ======================
# 💰 BUSINESS INPUT
# ======================
avg_order_value = st.number_input("💰 Avg Order Value (Rs)", value=3000)

# ======================
# 📊 KPIs
# ======================
total = len(df)
confirmed = len(df[df['status'] == 'Auto-Confirmed'])
risk = len(df[df['status'] == 'Risk Flagged'])
rejected = len(df[df['status'] == 'Rejected'])
high_risk = len(df[df.get('risk_level', '') == 'HIGH'])

avg_risk = round(df['risk_score'].mean(), 1) if 'risk_score' in df.columns else 0

loss = rejected * avg_order_value
risk_amount = risk * avg_order_value

# ======================
# 📊 KPI ROW (COMPACT)
# ======================
k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Orders", total)
k2.metric("Confirmed", confirmed)
k3.metric("Risk", risk)
k4.metric("Rejected", rejected)
k5.metric("High Risk", high_risk)
k6.metric("Avg Risk", avg_risk)

k7, k8 = st.columns(2)

k7.metric("💸 Loss", f"Rs {loss:,}")
k8.metric("⚠️ At Risk", f"Rs {risk_amount:,}")

st.divider()

# ======================
# 📊 COMPACT ANALYTICS
# ======================
c1, c2, c3 = st.columns([1,1,1])

# 🍩 SMALL DONUT
with c1:
    st.markdown("#### Status")

    status_counts = df['status'].value_counts()

    fig, ax = plt.subplots(figsize=(2.5,2.5))

    ax.pie(
        status_counts,
        labels=None,
        autopct='%1.0f%%',
        textprops={'fontsize':8}
    )

    centre = plt.Circle((0,0),0.65,fc='white')
    fig.gca().add_artist(centre)

    st.pyplot(fig, use_container_width=True)

# 📊 CITY CHART
with c2:
    st.markdown("#### Cities")

    if 'city' in df.columns:
        city_counts = df['city'].value_counts().head(5)

        fig2, ax2 = plt.subplots(figsize=(3,2))
        ax2.barh(city_counts.index, city_counts.values)
        ax2.tick_params(labelsize=8)

        st.pyplot(fig2, use_container_width=True)

# 🧠 INSIGHTS
with c3:
    st.markdown("#### Insights")

    risk_pct = round((risk/total)*100,1) if total > 0 else 0

    top_city = df['city'].value_counts().idxmax() if 'city' in df.columns else "N/A"

    st.markdown(f"""
    **Top City:** {top_city}  
    **Risk Rate:** {risk_pct}%  
    **Loss:** Rs {loss:,}  
    """)

    if risk_pct > 50:
        st.error("High Risk 🚨")
    elif risk_pct > 30:
        st.warning("Moderate Risk ⚠️")
    else:
        st.success("Healthy ✅")

# ======================
# 🎛 FILTERS
# ======================
st.subheader("Filters")

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
st.caption("Refreshing every 15 seconds...")
time.sleep(15)
st.rerun()

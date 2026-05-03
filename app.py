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
# 🎯 COMPACT KPI CARDS
# ======================
st.markdown("### 📊 Overview")

k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Orders", total)
k2.metric("Confirmed", confirmed)
k3.metric("Risk", risk)
k4.metric("Rejected", rejected)
k5.metric("High Risk", high_risk)
k6.metric("Avg Risk", avg_risk)

st.divider()

# ======================
# 📊 COMPACT ANALYTICS ROW
# ======================
c1, c2, c3 = st.columns([1,1,1])

# 🍩 SMALL DONUT (FIXED SIZE)
with c1:
    st.markdown("#### Status")

    status_counts = df['status'].value_counts()

    fig, ax = plt.subplots(figsize=(2.5,2.5))  # 👈 SMALL SIZE

    ax.pie(
        status_counts,
        labels=None,  # 👈 REMOVE LABEL CLUTTER
        autopct='%1.0f%%',
        textprops={'fontsize':8}
    )

    centre = plt.Circle((0,0),0.65,fc='white')
    fig.gca().add_artist(centre)

    ax.set_title("", fontsize=8)

    st.pyplot(fig, use_container_width=True)

# 📊 SMALL BAR CHART
with c2:
    st.markdown("#### Cities")

    city_counts = df['city'].value_counts().head(5)

    fig2, ax2 = plt.subplots(figsize=(3,2))  # 👈 SMALL
    ax2.barh(city_counts.index, city_counts.values)
    ax2.tick_params(labelsize=8)

    st.pyplot(fig2, use_container_width=True)

# 🧠 MICRO INSIGHTS PANEL
with c3:
    st.markdown("#### Insights")

    risk_pct = round((risk/total)*100,1) if total > 0 else 0

    top_city = df['city'].value_counts().idxmax()

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

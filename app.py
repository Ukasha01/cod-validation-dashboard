import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ======================
# 🎨 CLEAN UI HEADER
# ======================
st.markdown("""
    <h1 style='text-align: center; color: #2c3e50;'>📦 COD Validation Dashboard</h1>
    <p style='text-align: center; color: gray;'>AI-powered Order Intelligence System</p>
""", unsafe_allow_html=True)

url = st.text_input("https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv")

# ======================
# 📥 LOAD DATA
# ======================
csv_url = "https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv"

try:
    df = pd.read_csv(csv_url)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Remove empty columns
    df = df.dropna(axis=1, how='all')

    # Keep only important rows
    required_columns = ['status', 'city', 'address']
    df = df.dropna(subset=[col for col in required_columns if col in df.columns])

except Exception as e:
    st.error(f"Error loading data: {e}")
    df = pd.DataFrame()

        # ======================
        # 📊 SMART STATS
        # ======================
    total = len(df)
    confirmed = len(df[df['status'] == 'Auto-Confirmed'])
    risk = len(df[df['status'] == 'Risk Flagged'])
    rejected = len(df[df['status'] == 'Rejected'])

    high_risk = len(df[df['risk_level'] == 'HIGH']) if 'risk_level' in df.columns else 0

    rejection_rate = round((rejected / total) * 100, 2)
    risk_rate = round((risk / total) * 100, 2)

    top_city = df['city'].mode()[0] if 'city' in df.columns else "N/A"

    avg_risk = round(df['risk_score'].mean(), 1) if 'risk_score' in df.columns else 0

        # ======================
        # 📊 METRICS UI
        # ======================
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("📦 Orders", total)
    col2.metric("✅ Confirmed", confirmed)
    col3.metric("⚠️ Risk", risk, f"{risk_rate}%")
    col4.metric("❌ Rejected", rejected, f"{rejection_rate}%")
    col5.metric("🔥 High Risk", high_risk)
    col6.metric("📊 Avg Risk", avg_risk)

    st.divider()

        # ======================
        # 🎨 STYLE FUNCTIONS
        # ======================
    def color_status(val):
        if val == "Rejected":
                return "background-color: #fdecea; color: #c0392b; font-weight: bold;"
        elif val == "Risk Flagged":
                return "background-color: #fff4e5; color: #e67e22; font-weight: bold;"
        elif val == "Auto-Confirmed":
                return "background-color: #eafaf1; color: #27ae60; font-weight: bold;"
            

        def color_risk(val):
            if val == "HIGH":
                return "background-color: #f8d7da; color: #721c24;"
            elif val == "MEDIUM":
                return "background-color: #fff3cd; color: #856404;"
            elif val == "LOW":
                return "background-color: #d4edda; color: #155724;"
            return ""

        # ======================
        # 📋 FILTER (PRO FEATURE)
        # ======================
        filter_status = st.selectbox("Filter by Status", ["All", "Auto-Confirmed", "Risk Flagged", "Rejected"])

        if filter_status != "All":
            df = df[df['status'] == filter_status]

        # ======================
        # 🎨 APPLY STYLING
        # ======================
        styled_df = df.style

        if 'status' in df.columns:
            styled_df = styled_df.map(color_status, subset=['status'])

        if 'risk_level' in df.columns:
            styled_df = styled_df.map(color_risk, subset=['risk_level'])

        # ======================
        # 📋 FINAL TABLE
        # ======================
        st.subheader("📋 Orders Overview")
        st.dataframe(styled_df, use_container_width=True)

 

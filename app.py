import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📦 COD Order Validation Dashboard")

url = st.text_input("https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv")

if url:
    try:
        df = pd.read_csv(url)

        # Clean columns
        df.columns = df.columns.str.strip().str.lower()

        if df.empty:
            st.warning("⚠️ No data available")
            st.stop()

        st.success("✅ Data Loaded")

        # ======================
        # 📊 IMPORTANT STATS
        # ======================
        total = len(df)
        confirmed = len(df[df['status'] == 'Auto-Confirmed'])
        risk = len(df[df['status'] == 'Risk Flagged'])
        rejected = len(df[df['status'] == 'Rejected'])

        rejection_rate = round((rejected / total) * 100, 2)
        risk_rate = round((risk / total) * 100, 2)

        top_city = df['city'].value_counts().idxmax() if 'city' in df.columns else "N/A"

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total Orders", total)
        col2.metric("Rejected ❌", rejected, f"{rejection_rate}%")
        col3.metric("Risk ⚠️", risk, f"{risk_rate}%")
        col4.metric("Confirmed ✅", confirmed)
        col5.metric("Top City 🏙️", top_city)

        st.divider()

        # ======================
        # 🎨 COLUMN COLORING
        # ======================

        def color_status(val):
            if val == "Rejected":
                return "background-color: #ffcccc; color: black;"
            elif val == "Risk Flagged":
                return "background-color: #fff3cd; color: black;"
            elif val == "Auto-Confirmed":
                return "background-color: #d4edda; color: black;"
            return ""

        def color_risk(val):
            if val == "HIGH":
                return "background-color: #ff9999"
            elif val == "MEDIUM":
                return "background-color: #ffe599"
            elif val == "LOW":
                return "background-color: #c6efce"
            return ""

        styled_df = df.style.map(color_status, subset=['status'])

        if 'risk_level' in df.columns:
            styled_df = styled_df.map(color_risk, subset=['risk_level'])

        # ======================
        # 📋 TABLE
        # ======================
        st.subheader("📋 Orders")
        st.dataframe(styled_df, use_container_width=True)

    except Exception as e:
        st.error("❌ Error loading data")
        st.text(str(e))

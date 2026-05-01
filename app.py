import streamlit as st
import pandas as pd

st.set_page_config(page_title="COD Dashboard", layout="wide")

# 🎨 UI Styling
st.markdown("""
<style>
body { background-color: #0E1117; }

.section {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.green { background-color: #1f7a4d; color: white; }
.red { background-color: #8b1e1e; color: white; }
.orange { background-color: #b36b00; color: white; }
.blue { background-color: #1e3a8a; color: white; }

</style>
""", unsafe_allow_html=True)

# 🧠 Title
st.title("📦 COD Order Validation Dashboard")

# 🔗 Input
url = st.text_input("https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv")

if url:
    try:
        df = pd.read_csv(url)

        # 🔥 Clean column names
        df.columns = df.columns.str.strip().str.lower()

        # 🔍 DEBUG
        st.write("📊 Raw Data Preview", df)

        if df.empty:
            st.warning("⚠️ No data found in sheet")
            st.stop()

        st.success("✅ Data Loaded Successfully")

        # 📊 KPIs
        total = len(df)
        confirmed = len(df[df['status'] == 'Auto-Confirmed'])
        risk = len(df[df['status'] == 'Risk Flagged'])
        rejected = len(df[df['status'] == 'Rejected'])

        # 🎯 KPI ROW
        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f'<div class="section blue"><h3>Total Orders</h3><h1>{total}</h1></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="section green"><h3>Confirmed</h3><h1>{confirmed}</h1></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="section orange"><h3>Risk</h3><h1>{risk}</h1></div>', unsafe_allow_html=True)
        col4.markdown(f'<div class="section red"><h3>Rejected</h3><h1>{rejected}</h1></div>', unsafe_allow_html=True)

        st.markdown("---")

        # 🔍 FILTER SECTION
        st.markdown("### 🔍 Filter Orders")
        status_filter = st.selectbox("Select Status", ["All"] + list(df['status'].dropna().unique()))

        if status_filter != "All":
            df = df[df['status'] == status_filter]

        # 🎨 COLOR TABLE
        def highlight(row):
            if row['status'] == 'Rejected':
                return ['background-color: #ff4d4d'] * len(row)
            elif row['status'] == 'Risk Flagged':
                return ['background-color: #ffa64d'] * len(row)
            elif row['status'] == 'Auto-Confirmed':
                return ['background-color: #66cc99'] * len(row)
            return [''] * len(row)

        # 📋 TABLE SECTION
        st.markdown("### 📋 Orders Table")
        st.dataframe(df.style.apply(highlight, axis=1), use_container_width=True)

    except Exception as e:
        st.error("❌ Error loading data")
        st.text(str(e))

else:
    st.info("👉 Paste your CSV link to start")

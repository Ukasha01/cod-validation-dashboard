import streamlit as st
import pandas as pd

st.set_page_config(page_title="COD Dashboard", layout="wide")

# 🎨 Custom CSS (UI Styling)
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.block-container {
    padding-top: 2rem;
}
.card {
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
}
.green {background-color: #1f7a4d;}
.red {background-color: #8b1e1e;}
.orange {background-color: #b36b00;}
</style>
""", unsafe_allow_html=True)

# 🧠 Title
st.title("📦 COD Order Validation Dashboard")

# 🔗 Input
url = st.text_input("https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv")

if url:
    try:
        df = pd.read_csv(url)

        # ✅ FIX COLUMN NAMES
        df.columns = df.columns.str.strip().str.lower()

        st.success("✅ Data Loaded Successfully")

        # 🔍 DEBUG (optional)
        st.write("Columns:", df.columns)

        # ✅ CHECK REQUIRED COLUMN
        if "status" not in df.columns:
            st.error("❌ Missing 'status' column in sheet")
            st.stop()

        # 📊 KPI
        total = len(df)
        confirmed = len(df[df['status'] == 'Auto-Confirmed'])
        risk = len(df[df['status'] == 'Risk Flagged'])
        rejected = len(df[df['status'] == 'Rejected'])

        st.write("Total:", total)

    except Exception as e:
        st.error("❌ Failed to load data")
        st.text(str(e))

else:
    st.info("👉 Paste your CSV link to view dashboard")

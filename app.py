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

        st.success("✅ Data Loaded Successfully")

        # 📊 KPI CARDS
        total = len(df)
        confirmed = len(df[df['status'] == 'Auto-Confirmed'])
        risk = len(df[df['status'] == 'Risk Flagged'])
        rejected = len(df[df['status'] == 'Rejected'])

        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f'<div class="card green">Total Orders<br><h2>{total}</h2></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="card green">Confirmed<br><h2>{confirmed}</h2></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="card orange">Risk<br><h2>{risk}</h2></div>', unsafe_allow_html=True)
        col4.markdown(f'<div class="card red">Rejected<br><h2>{rejected}</h2></div>', unsafe_allow_html=True)

        st.markdown("---")

        # 🔍 FILTER
        st.subheader("🔍 Filter Orders")
        status_filter = st.selectbox("Select Status", ["All"] + list(df['status'].unique()))

        if status_filter != "All":
            df = df[df['status'] == status_filter]

        # 🎨 TABLE COLOR FUNCTION
        def highlight_rows(row):
            if row['status'] == 'Rejected':
                return ['background-color: #ff4d4d'] * len(row)
            elif row['status'] == 'Risk Flagged':
                return ['background-color: #ffa64d'] * len(row)
            elif row['status'] == 'Auto-Confirmed':
                return ['background-color: #66cc99'] * len(row)
            else:
                return [''] * len(row)

        st.subheader("📋 Orders Table")

        st.dataframe(
            df.style.apply(highlight_rows, axis=1),
            use_container_width=True
        )

    except Exception as e:
        st.error("❌ Failed to load data")
        st.text(str(e))

else:
    st.info("👉 Paste your CSV link to view dashboard")

import streamlit as st
import pandas as pd

st.set_page_config(page_title="COD Dashboard", layout="wide")

st.title("📦 COD Order Validation Dashboard")

url = st.text_input("import streamlit as st")
import pandas as pd

st.set_page_config(page_title="COD Dashboard", layout="wide")

st.title("📦 COD Order Validation Dashboard")

url = st.text_input("https://docs.google.com/spreadsheets/d/1QXHOICBrv0zMk5nFFqTWxg43p4_mA5ENxk6rBoXEXyI/export?format=csv")

if url:
    try:
        df = pd.read_csv(url)

        st.success("✅ Data Loaded Successfully")

        st.subheader("📊 Data Preview")
        st.dataframe(df)

        # KPIs
        st.subheader("📈 Insights")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Orders", len(df))
        col2.metric("Rejected", len(df[df['status'] == 'Rejected']))
        col3.metric("Risk Orders", len(df[df['status'] == 'Risk Flagged']))

        # Filter
        st.subheader("🔍 Filter by Status")
        status_filter = st.selectbox("Select Status", df['status'].unique())

        filtered_df = df[df['status'] == status_filter]
        st.dataframe(filtered_df)

    except Exception as e:
        st.error("❌ Failed to load data. Check your CSV link or permissions.")
        st.text(str(e))

else:
    st.warning("⚠️ Please paste your CSV URL above to load dashboard")")

if url:
    try:
        df = pd.read_csv(url)

        st.success("✅ Data Loaded Successfully")

        st.subheader("📊 Data Preview")
        st.dataframe(df)

        # KPIs
        st.subheader("📈 Insights")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Orders", len(df))
        col2.metric("Rejected", len(df[df['status'] == 'Rejected']))
        col3.metric("Risk Orders", len(df[df['status'] == 'Risk Flagged']))

        # Filter
        st.subheader("🔍 Filter by Status")
        status_filter = st.selectbox("Select Status", df['status'].unique())

        filtered_df = df[df['status'] == status_filter]
        st.dataframe(filtered_df)

    except Exception as e:
        st.error("❌ Failed to load data. Check your CSV link or permissions.")
        st.text(str(e))

else:
    st.warning("⚠️ Please paste your CSV URL above to load dashboard")
